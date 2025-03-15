from domain.user.exceptions.fullname import (
    NameIsTooLongException,
    NameIsTooShortException,
    WrongNameFormatException,
)
from domain.user.exceptions.username import (
    UsernameIsTooLongException,
    UsernameIsTooShortException,
    WrongUsernameFormatException,
)
from domain.user.values.fullname import FullName
from domain.user.values.is_deleted import DeletedAt
from domain.user.values.user_id import UserId
from domain.user.values.username import Username

import pytest


def test_fullname():
    fullname = FullName("first_name", "last_name", "middle_name")

    assert fullname.first_name == "first_name"
    assert fullname.last_name == "last_name"
    assert fullname.middle_name == "middle_name"


def test_is_deleted():
    deleted_at = DeletedAt.not_deleted()

    assert deleted_at.is_deleted() is False


def test_user_id():
    user_id = UserId("123")

    assert user_id.to_raw() == "123"


def test_username():
    username = Username("username")

    assert username.to_raw() == "username"


def test_username_is_too_long():
    with pytest.raises(UsernameIsTooLongException):
        Username("12345678901234567890123456789012345678901234567890")


def test_username_is_too_short():
    with pytest.raises(UsernameIsTooShortException):
        Username("")


def test_fullname_is_too_long():
    with pytest.raises(NameIsTooLongException):
        FullName("12345678901234567890123456789012345678901234567890", "asdasdasd")


def test_fullname_is_too_short():
    with pytest.raises(NameIsTooShortException):
        FullName("", "asdasdasd")


def test_username_is_not_valid():
    with pytest.raises(WrongUsernameFormatException):
        Username("123")


def test_fullname_is_not_valid():
    with pytest.raises(WrongNameFormatException):
        FullName("123", "asdasdasd")
