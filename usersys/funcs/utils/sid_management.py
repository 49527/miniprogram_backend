"""
SID management functions

Created by Hangyu Fan, May 6, 2018

Last modified: May 8, 2018
"""
import uuid
from usersys.models import UserSid
from django.utils.timezone import now


def get_sid(sidstr, ignore_expire=False):
    try:
        if ignore_expire:
            sid = UserSid.objects.get(sid=sidstr, is_login=True)
        else:
            sid = UserSid.objects.get(sid=sidstr, is_login=True, expire_datetime__gte=now())
    except UserSid.DoesNotExist:
        return None

    return sid


def sid_to_user(sid, ignore_expire=False):
    # TODO: Cache sid-user map
    sidobj = get_sid(sid, ignore_expire)

    return sidobj.uid if sidobj is not None else None


def sid_create(user, ipaddr, session_key, duration):
    sid = UserSid.objects.create(
        sid=str(uuid.uuid1()),
        uid=user,
        last_ipaddr=ipaddr,
        is_login=True,
        expire_datetime=now() + duration,
        last_login=now(),
        session_key=session_key
    )
    return sid.sid


def sid_reuse(user, ipaddr, session_key):
    """
    return the latest reusable user_sid.
    :param user: user object
    :param ipaddr: ip address
    :param session_key: session key
    :return: None if not reusable, else the usersid string.
    """
    try:
        sid_reusable = UserSid.objects.filter(
            uid=user,
            # last_ipaddr=ipaddr, # Wechat Mini program's frontend uses random ip addresses.
            is_login=True,
            session_key=session_key,
            expire_datetime__gte=now(),
        ).latest("last_login")
        return sid_reusable
    except UserSid.DoesNotExist:
        return None


def sid_access(sid):
    """
    if user access the sid, please call this function
    :param sid:
    """
    # TODO: hook this function into sid model, maybe
    if isinstance(sid, (str, unicode)):
        try:
            sidobj = UserSid.objects.get(sid=sid)
            sidobj.last_login = now()
            sidobj.save()
        except UserSid.DoesNotExist:
            pass
    elif isinstance(sid, UserSid):
        sid.last_login = now()
        sid.save()
    else:
        raise TypeError


def sid_destroy(sid):
    """
    Set sid is_login to False
    :param sid:
    :return:
    """
    sidobj = get_sid(sid)
    if sidobj is not None:
        sidobj.is_login = False
        sidobj.save()
        # TODO: Clean sid-user cache
    else:
        raise KeyError("Sid not exist")


def sid_getuser(sid, ignore_expire=False):
    """
    Get the corresponded user object.
    :param sid:
    :param ignore_expire:
    :return: corresponded user object
    """
    return sid_to_user(sid, ignore_expire)

