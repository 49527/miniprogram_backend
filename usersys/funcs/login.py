# coding=utf-8
import requests
import logging
import time
import uuid
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.core.cache import caches
from base.exceptions import *
from base.util.phone_validator import phone_validator
from base.util.misc_validators import validators
from base.util.temp_session import create_session, update_session_dict, \
    destroy_session, get_session_dict, get_session, update_session
from usersys.funcs.utils.sid_management import sid_create, sid_destroy, sid_reuse, sid_access
from usersys.models import UserBase, UserSid, WechatUserContext
from usersys.choices.state_choice import state_choice
from usersys.choices.model_choice import user_role_choice
from business_sys.models import RecyclingStaffInfo
from .session import RegistrationSessionKeys, ValidateStatus


User = get_user_model()
logger = logging.getLogger(__name__)


def wechat_login(code, ipaddr, pn):
    # get openid and session_key
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid={AppID}&secret={AppSecret}&js_code={code}' \
          '&grant_type=authorization_code'.format(code=code, **settings.MINIPROGRAM)

    re = requests.get(url=url)
    re_data = re.json()
    if 'errcode' in re_data:
        raise WLException(401, re_data['errmsg'])

    openid = re_data['openid']
    session_key = re_data["session_key"]

    try:
        user = WechatUserContext.objects.get(openid=openid).uid
        if user.is_active is False:
            raise WLException(code=404, message="This user is not active.")

    except WechatUserContext.DoesNotExist:
        user, created = UserBase.objects.get_or_create(
            internal_name=openid,
            defaults={
                "role": user_role_choice.CLIENT,
                "is_active": True,
            }
        )

        if created:
            logger.warning("wx login: openid=%s duplicated." % openid)

        WechatUserContext.objects.create(
            uid=user,
            nickname=openid,
            openid=openid,
        )

    if user.pn is None:
        state = state_choice.PN_NOT_BIND
        sid = get_sid_by_pn(pn, user)
        user_sid = None
    else:
        state = state_choice.PN_BIND
        sid = None
        if user.pn != pn:
            raise WLException(409, _("请输入注册时用的手机号"))

        sid_obj = sid_reuse(user, ipaddr, session_key)
        if sid_obj is not None:
            sid_access(sid_obj)
            user_sid = sid_obj.sid
        else:
            user_sid = login(user, ipaddr, session_key)

    return user_sid, state, sid


def login(user, ipaddr, session_key):

    sid = sid_create(user, ipaddr, session_key, settings.SID_DURATION)
    return sid


@default_exception(Error500)
def get_sid_by_pn(pn, user):
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
        RegistrationSessionKeys.USER_ID: user.id,
        RegistrationSessionKeys.VCODE_LAST_TIME: time.time()
    }
    update_session_dict(sid, session)

    create_session(sid=sid_reverse)
    update_session(sid_reverse, RegistrationSessionKeys.SID, sid)

    return sid


def validate_sid(sid, pn, vcode):
    try:
        session = get_session_dict(sid)
    except KeyError:
        raise Error404("Sid does not exist")

    if pn != session.get(RegistrationSessionKeys.PHONE_NUMBER):
        raise Error409("pn conflicts with sid")

    if session.get(RegistrationSessionKeys.VALIDATE_STATUS) == ValidateStatus.VALIDATE_FAILED:
        raise Error401("Validate code not match")

    userid = session.get(RegistrationSessionKeys.USER_ID)
    if userid is None:
        raise Error405(u"用户会话错误")

    try:
        user = UserBase.objects.get(id=userid)
    except UserBase.DoesNotExist:
        raise Error405(u"用户会话错误")

    if session.get(RegistrationSessionKeys.VALIDATE_STATUS) == ValidateStatus.VALIDATE_SUCCEEDED:
        register(sid, pn, user)
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
            register(sid, pn, user)
            return
        else:
            session[RegistrationSessionKeys.VALIDATE_STATUS] = ValidateStatus.VALIDATE_FAILED
            update_session_dict(sid, session)
            raise Error401("Validate code not match")

    raise Error500("Unexpected fork")


def register(sid, pn, user):
    try:
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


def recycling_staff_login(pn, pwd, ipaddr, session_key=None):
    if session_key is None:
        session_key = uuid.uuid4()
    user = authenticate(username=pn, password=pwd, role=user_role_choice.RECYCLING_STAFF) # type: UserBase
    if user is None:
        raise WLException(400, u"帐号或密码错误")
    sid_obj = sid_reuse(user, ipaddr, session_key)
    if sid_obj is not None:
        sid_access(sid_obj)
        sid = sid_obj.sid
    else:
        sid = login(user, ipaddr, session_key)

    try:
        recycle_type = user.recycling_staff_info.recycle_bin.r_b_type
    except RecyclingStaffInfo.DoesNotExist:
        raise WLException(401, u"用户未绑定回收站")

    return sid, recycle_type


def send_sms(pn):
    t = caches["sessions"].get(pn)
    if t:
        raise WLException(400, u"请求太频繁")
    vcode = phone_validator.generate_and_send(pn)
    caches["sessions"].set(pn, vcode, 60)


def forget_pwd(pn, new_pwd1, new_pwd2, vcode):
    if new_pwd1 != new_pwd2:
        raise WLException(400, u"新老密码不同!")
    if vcode != caches["sessions"].get(pn):
        raise WLException(401, u"验证码错误")
    try:
        user = UserBase.objects.get(internal_name=pn)
    except UserBase.DoesNotExist:
        raise WLException(404, u"用户不存在")
    user.set_password(new_pwd1)
    user.save()
    return user
