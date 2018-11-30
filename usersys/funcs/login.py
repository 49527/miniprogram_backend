from django.contrib.auth import get_user_model
from base.exceptions import *
from usersys.funcs.utils.sid_management import sid_create, sid_destroy
from usersys.models import UserBase, UserSid
from usersys.choices.state_choice import state_choice
from django.conf import settings
import requests

import time
from base.util.phone_validator import phone_validator
from base.util.misc_validators import validators
from base.util.temp_session import create_session, update_session_dict, \
    destroy_session, get_session_dict, get_session, update_session
from usersys.choices.model_choice import user_role_choice

from .session import RegistrationSessionKeys, ValidateStatus

User = get_user_model()


def login(code, ipaddr):
    # get openid and session_key
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid={AppID}&secret={AppSecret}&js_code={code}' \
          '&grant_type=authorization_code'.format(code=code, **settings.MINIPROGRAM)

    re = requests.get(url=url)
    re_data = re.json()
    if 'errcode' in re_data:
        raise WLException(401, re_data['errmsg'])

    try:
        user = UserBase.object.get(openid=re_data['openid'])
    except UserBase.DoesNotExist:
        user = UserBase.object.create(openid=re_data['openid'], nickname=re_data['openid'],
                                      role=user_role_choice.CLIENT)

    sid = sid_create(user, ipaddr, re_data['session_key'], settings.SID_DURATION)

    state = state_choice.PN_NOT_BIND if user.pn is None else state_choice.PN_BIND

    return sid, state


@default_exception(Error500)
def get_sid_by_pn(pn):
    # validate phone number format
    if not validators.validate(pn, "phone number"):
        raise Error401("Format of phone number is incorrect.")

    # Ensure that user did not access this api recently.
    sid_reverse = RegistrationSessionKeys.PN_2_SID % pn

    try:
        sid_exist = get_session(sid_reverse, RegistrationSessionKeys.SID)
    except KeyError:
        sid_exist = None

    if sid_exist is not None:
        try:
            session_exist = get_session_dict(sid_exist)
        except KeyError:
            session_exist = None
        # If we have a exist session, Then:
        # 1) If the user gives a wrong validation code, this api send the validation code again;
        # 2) If the user does not validate within MIN_INTERVAL, send validation code again;
        # 3) If the user has already successfully validated, but call this api again, re-validate;
        # Otherwise, do nothing.
        if session_exist is not None and not (
            session_exist.get(RegistrationSessionKeys.VALIDATE_STATUS) == ValidateStatus.VALIDATE_FAILED or (
                session_exist.get(RegistrationSessionKeys.VALIDATE_STATUS) == ValidateStatus.VALIDATE_SENT and
                time.time() - session_exist.get(RegistrationSessionKeys.VCODE_LAST_TIME, 0.0) > ValidateStatus.MIN_INTERVAL
            ) or session_exist.get(RegistrationSessionKeys.VALIDATE_STATUS) == ValidateStatus.VALIDATE_SUCCEEDED
        ):
            return sid_exist

        if session_exist is None:
            sid_exist = None

    # send validate message
    vcode = phone_validator.generate_and_send(pn)

    # save validate message into sid
    sid = sid_exist if sid_exist is not None else create_session()

    session = {
        RegistrationSessionKeys.VALIDATE_STATUS: ValidateStatus.VALIDATE_SENT,
        RegistrationSessionKeys.PHONE_NUMBER: pn,
        RegistrationSessionKeys.VCODE: vcode,
        RegistrationSessionKeys.VCODE_LAST_TIME: time.time()
    }
    update_session_dict(sid, session)

    create_session(sid=sid_reverse)
    update_session(sid_reverse, RegistrationSessionKeys.SID, sid)

    return sid


def validate_sid(sid, pn, vcode, user_sid):
    try:
        session = get_session_dict(sid)
    except KeyError:
        raise Error404("Sid does not exist")

    if pn != session.get(RegistrationSessionKeys.PHONE_NUMBER):
        raise Error409("pn conflicts with sid")

    if session.get(RegistrationSessionKeys.VALIDATE_STATUS) == ValidateStatus.VALIDATE_FAILED:
        raise Error401("Validate code not match")

    if session.get(RegistrationSessionKeys.VALIDATE_STATUS) == ValidateStatus.VALIDATE_SUCCEEDED:
        register(sid, pn, user_sid)
        return

    if session.get(RegistrationSessionKeys.VALIDATE_STATUS) is None:
        # should not happen but cleanup in case
        destroy_session(sid)
        destroy_session(RegistrationSessionKeys.PN_2_SID % pn)
        raise Error404("Sid does not exist")

    if session.get(RegistrationSessionKeys.VALIDATE_STATUS) == ValidateStatus.VALIDATE_SENT:
        if session.get(RegistrationSessionKeys.VCODE) == vcode:
            session[RegistrationSessionKeys.VALIDATE_STATUS] = ValidateStatus.VALIDATE_SUCCEEDED
            update_session_dict(sid, session)
            register(sid, pn, user_sid)
            return
        else:
            session[RegistrationSessionKeys.VALIDATE_STATUS] = ValidateStatus.VALIDATE_FAILED
            update_session_dict(sid, session)
            raise Error401("Validate code not match")

    raise Error500("Unexpected fork")


def register(sid, pn, user_sid):
    try:
        user = UserSid.objects.get(sid=user_sid).uid
        user.pn = pn
        user.is_active = True
        user.save()
        # destroy sid
        destroy_session(sid)
    except UserSid.DoesNotExist:
        raise WLException(400, 'user_sid error')


def logout(user_sid):
    try:
        sid_destroy(user_sid)
    except KeyError:
        raise WLException(404, "user_id do not exist")
