from domain.user.events.user_deleted import UserDeleted
from domain.user.events.fullname_updated import FullnameUpdated
from domain.user.events.username_updated import UsernameUpdated
from domain.user.events.user_created import UserCreated
from domain.user.events.user_restored import UserRestored
from domain.user.values.is_deleted import DeletedAt
from domain.user.values.fullname import FullName
from domain.user.values.user_id import UserId
from domain.user.values.username import Username
from domain.user.exceptions.user import UserIsDeletedException
from domain.user.entities.user import User
import pytest


def test_create_user():
    user_id = UserId("123")
    username = Username("username")
    fullname = FullName("first_name", "last_name", "middle_name")

    user = User.create(user_id, username, fullname)

    assert user.id == user_id
    assert user.username == username
    assert user.fullname == fullname

    assert isinstance(user.deleted_at, DeletedAt)
    assert user.deleted_at.is_deleted() is False

    assert isinstance(user._events[0], UserCreated)


def test_delete_user():
    user_id = UserId("123")
    username = Username("username")
    fullname = FullName("first_name", "last_name", "middle_name")

    user = User.create(user_id, username, fullname)

    user.delete()

    assert user.deleted_at.is_deleted() is True

    assert isinstance(user._events[1], UserDeleted)


def test_restore_user():
    user_id = UserId("123")
    username = Username("username")
    fullname = FullName("first_name", "last_name", "middle_name")

    user = User.create(user_id, username, fullname)

    user.delete()
    user.restore()

    assert user.deleted_at.is_deleted() is False

    assert isinstance(user._events[-1], UserRestored)


def test_set_fullname():
    user_id = UserId("123")
    username = Username("username")
    fullname = FullName("first_name", "last_name", "middle_name")

    user = User.create(user_id, username, fullname)

    user.set_fullname(FullName("new_first_name", "new_last_name", "new_middle_name"))

    assert user.fullname == FullName(
        "new_first_name", "new_last_name", "new_middle_name"
    )

    assert isinstance(user._events[-1], FullnameUpdated)


def test_set_username():
    user_id = UserId("123")
    username = Username("username")
    fullname = FullName("first_name", "last_name", "middle_name")

    user = User.create(user_id, username, fullname)

    user.set_username(Username("new_username"))

    assert user.username == Username("new_username")

    assert isinstance(user._events[-1], UsernameUpdated)


def test_change_deleted_username():
    user_id = UserId("123")
    username = Username("username")
    fullname = FullName("first_name", "last_name", "middle_name")

    user = User.create(user_id, username, fullname)

    user.delete()
    with pytest.raises(UserIsDeletedException):
        user.set_username(Username("new_username"))


def test_middle_name_not_received():
    user_id = UserId("123")
    username = Username("username")
    fullname = FullName("first_name", "last_name")

    user = User.create(user_id, username, fullname)

    assert user.fullname == FullName("first_name", "last_name")
    assert user.fullname.middle_name is None
