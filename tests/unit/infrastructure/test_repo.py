from sqlalchemy.ext.asyncio import AsyncSession

from domain.user.entities.user import User
from domain.user.values.fullname import FullName
from domain.user.values.user_id import UserId
from domain.user.values.username import Username
from infrastructure.base.repository.base import SQLAlchemyRepository
from infrastructure.base.repository.user_reader import BaseUserReader
from infrastructure.base.repository.user_writer import BaseUserWriter
from infrastructure.db.uow import SQLAlchemyUoW
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncEngine
from infrastructure.db.models import BaseModel
from infrastructure.exceptions import UserDoesNotExistException
from infrastructure.repositories import UserReader
from sqlalchemy.exc import IntegrityError

from infrastructure.repositories.pagination import Pagination


async def test_create_user(di_container):

    user = User.create(
        UserId("test_user_id"),
        Username("test_username"),
        FullName("test_first_name", "test_last_name", "test_middle_name"),
    )

    async with di_container() as c:
        user_writer = await c.get(BaseUserWriter)
        uow = await c.get(SQLAlchemyUoW)

        await user_writer.create_user(user)
        await uow.commit()

    async with di_container() as c:
        user_reader = await c.get(BaseUserReader)
        db_user = await user_reader.get_user_by_id(user_id=user.id.to_raw())

        assert db_user is not None
        assert db_user.id.to_raw() == user.id.to_raw()
        assert db_user.username.to_raw() == user.username.to_raw()


async def test_user_with_used_username_creation(create_test_user, di_container):
    user = User.create(
        UserId("user_id"),
        Username("username"),
        FullName("first_name", "last_name", "middle_name"),
    )

    async with di_container() as c:
        user_writer = await c.get(BaseUserWriter)
        with pytest.raises(IntegrityError):
            user = await user_writer.create_user(user=user)


async def test_update_username(create_test_user, di_container):
    user = User.create(
        UserId("user_id"),
        Username("new_username"),
        FullName("first_name", "last_name", "middle_name"),
    )

    async with di_container() as c:
        user_writer = await c.get(BaseUserWriter)
        user_reader = await c.get(BaseUserReader)
        uow = await c.get(SQLAlchemyUoW)

        await user_writer.update_user(user=user)
        await uow.commit()

        updated_user = await user_reader.get_user_by_id(user_id="user_id")

        assert updated_user.username.to_raw() == "new_username"


async def test_get_user_by_username(di_container):
    """Test retrieving a user by username"""
    async with di_container() as c:
        user_writer = await c.get(BaseUserWriter)
        uow = await c.get(SQLAlchemyUoW)

        # Create test user
        user = User.create(
            UserId("username_lookup_id"),
            Username("find_me_by_username"),
            FullName("Alice", "Johnson", "Marie"),
        )
        await user_writer.create_user(user=user)
        await uow.commit()

    # Get user
    async with di_container() as c2:
        user_reader = await c2.get(BaseUserReader)

        # Lookup by username
        found_user = await user_reader.get_user_by_username(
            username="find_me_by_username"
        )
        assert found_user is not None
        assert found_user.id.to_raw() == "username_lookup_id"
        assert found_user.fullname.first_name == "Alice"


async def test_user_not_found(di_container):
    """Test handling non-existent users"""
    async with di_container() as c:
        user_reader = await c.get(BaseUserReader)

        # Try to find not existent user then get an exception
        with pytest.raises(UserDoesNotExistException):
            await user_reader.get_user_by_id(user_id="does_not_exist")


async def test_delete_user(create_test_user, di_container):
    """Test deleting a user"""
    async with di_container() as c:
        user_writer = await c.get(BaseUserWriter)
        user_reader = await c.get(BaseUserReader)
        uow = await c.get(SQLAlchemyUoW)

        # Verify the user exists first
        existing_user = await user_reader.get_user_by_id(user_id="user_id")
        assert existing_user is not None

        # Delete the user
        existing_user.delete()
        await user_writer.delete_user(existing_user)
        await uow.commit()

    async with di_container() as c:
        # Verify deletion
        user_reader = await c.get(BaseUserReader)

        deleted_user = await user_reader.get_user_by_id(user_id="user_id")
        assert deleted_user.deleted_at.is_deleted() is True


async def test_restore_user_back_to_active(create_test_user, di_container):
    """Test restoring a user back to active"""
    async with di_container() as c:
        user_writer = await c.get(BaseUserWriter)
        user_reader = await c.get(BaseUserReader)
        uow = await c.get(SQLAlchemyUoW)

        # Verify the user exists first
        existing_user = await user_reader.get_user_by_id(user_id="user_id")
        assert existing_user is not None

        # Restore the user
        existing_user.restore()
        await user_writer.restore_user(existing_user)
        await uow.commit()

    async with di_container() as c:
        # Verify restoration
        user_reader = await c.get(BaseUserReader)
        restored_user = await user_reader.get_user_by_id(user_id="user_id")
        assert restored_user.deleted_at.is_deleted() is False


async def test_update_full_name(create_test_user, di_container):
    """Test updating a user's full name"""
    async with di_container() as c:
        user_writer = await c.get(BaseUserWriter)
        user_reader = await c.get(BaseUserReader)
        uow = await c.get(SQLAlchemyUoW)

        # Get the existing user
        user = await user_reader.get_user_by_id(user_id="user_id")

        # Update full name
        user.set_fullname(fullname=FullName("Updated", "Name", "Changed"))

        await user_writer.update_user(user=user)
        await uow.commit()

    async with di_container() as c:
        # Verify update
        user_reader = await c.get(BaseUserReader)
        result = await user_reader.get_user_by_id(user_id="user_id")
        assert result.fullname.first_name == "Updated"
        assert result.fullname.last_name == "Name"
        assert result.fullname.middle_name == "Changed"


async def test_list_all_users(di_container):
    """Test listing all users with pagination"""
    async with di_container() as c:
        user_writer = await c.get(BaseUserWriter)
        user_reader = await c.get(BaseUserReader)
        uow = await c.get(SQLAlchemyUoW)

        # Create multiple test users
        for i in range(5):
            user = User.create(
                UserId(f"list_user_{i}"),
                Username(f"list_username_{i}"),
                FullName(f"First{i}", f"Last{i}", f"Middle{i}"),
            )
            await user_writer.create_user(user=user)

        await uow.commit()
    async with di_container() as c:
        user_reader = await c.get(BaseUserReader)
        pagination1 = Pagination(offset=0, limit=2)
        pagination2 = Pagination(offset=2, limit=3)

        # Test listing with pagination
        page_1 = await user_reader.get_all_users(pagination=pagination1)
        assert len(page_1) == 2

        page_2 = await user_reader.get_all_users(pagination=pagination2)
        assert len(page_2) == 3

        # Ensure no duplicates between pages
        page_1_ids = {user.id.to_raw() for user in page_1}
        page_2_ids = {user.id.to_raw() for user in page_2}
        assert not page_1_ids.intersection(page_2_ids)


async def test_transaction_rollback_on_error(di_container):
    """Test transaction rollback when an error occurs"""
    async with di_container() as c:
        user_writer = await c.get(BaseUserWriter)
        user_reader = await c.get(BaseUserReader)
        uow = await c.get(SQLAlchemyUoW)

        # Create initial valid user
        valid_user = User.create(
            UserId("rollback_test_id"),
            Username("rollback_username"),
            FullName("First", "Last", "Middle"),
        )

        # Create a duplicate user that will cause integrity error
        duplicate_user = User.create(
            UserId("another_id"),
            Username("rollback_username"),  # Same username will cause conflict
            FullName("Other", "Person", "Name"),
        )

        try:
            # Add both users in the same transaction
            await user_writer.create_user(user=valid_user)
            await user_writer.create_user(user=duplicate_user)  # This should fail
            await uow.commit()
            pytest.fail("Expected IntegrityError was not raised")

        except IntegrityError:
            await uow.rollback()

    async with di_container() as c:
        user_reader = await c.get(BaseUserReader)
        # Verify that neither user was added (transaction rolled back)

        with pytest.raises(UserDoesNotExistException):
            await user_reader.get_user_by_id(user_id="another_id")

        with pytest.raises(UserDoesNotExistException):
            await user_reader.get_user_by_id(user_id="rollback_test_id")
