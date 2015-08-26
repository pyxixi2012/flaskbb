from flask import current_app
from flaskbb import exceptions as excs
from flaskbb.extensions import db
from flaskbb.user.models import User, groups_users, Group
from flaskbb.utils.helpers import get_online_users
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound


def get_online(count_only=False):
    if current_app.config['REDIS_ENABLED']:
        online_users = get_online_users()
        online_guests = get_online_users(guest=True)

        if count_only:
            online_users, online_guests = len(online_users), len(online_guests)
    else:
        if count_only:
            online_users = User.online_user_count()
        else:
            online_users = User.online_users()
        online_guests = 0

    return online_users, online_guests


def total_users():
    return User.total_users()


def fetch_by_email(email):
    try:
        return User.query.filter_by(email=email).one()
    except NoResultFound:
        raise excs.NotFound("The requested user was not found.")


def fetch_by_username(username):
    try:
        return User.query.filter_by(username=username).one()
    except NoResultFound:
        raise excs.NotFound("The requested user was not found.")


def fetch(id):
    return User.query.get(id)


def in_group(user, group):
    return User.query.with_entities(User.id).filter(
        db.or_(user.primary_group.id == group.id,
               groups_users.c.group_id == group.id)
    ).count() > 0


def ban(user):
    user.primary_group = Group.banned_group
    user.invalidate_cache()


def unban(user):
    user.primary_group = Group.member_group
    user.invalidate_cache()
