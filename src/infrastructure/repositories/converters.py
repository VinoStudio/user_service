import infrastructure.db.models.user as models
import domain.user.entities.user as entities
from domain.user.values.user_id import UserId
from domain.user.values.is_deleted import DeletedAt
from domain.user.values.fullname import FullName
from domain.user.values.username import Username
from infrastructure.exceptions.repository import UserIsDeletedException


def convert_db_model_to_user_entity(user: models.User) -> entities.User:
    fullname = FullName(
        first_name=user.first_name,
        last_name=user.last_name,
        middle_name=user.middle_name,
    )
    return entities.User(
        id=UserId(user.id),
        username=Username(user.username),
        fullname=fullname,
        deleted_at=DeletedAt(user.deleted_at),
        version=user.version,
    )


def convert_db_model_to_active_user_entity(user: models.User) -> entities.User:
    if user.deleted_at is not None:
        raise UserIsDeletedException(user.id)

    fullname = FullName(
        first_name=user.first_name,
        last_name=user.last_name,
        middle_name=user.middle_name,
    )
    return entities.User(
        id=UserId(user.id),
        username=Username(user.username),
        fullname=fullname,
        deleted_at=DeletedAt(user.deleted_at),
        version=user.version,
    )


def convert_user_entity_to_db_model(user: entities.User) -> models.User:
    return models.User(
        id=user.id.to_raw(),
        username=user.username.to_raw(),
        first_name=user.fullname.first_name,
        last_name=user.fullname.last_name,
        middle_name=user.fullname.middle_name,
        deleted_at=user.deleted_at.value,
        version=user.version,
    )


def convert_user_entity_to_db_dict(user: entities.User) -> dict:
    return dict(
        id=user.id.to_raw(),
        username=user.username.to_raw(),
        first_name=user.fullname.first_name,
        last_name=user.fullname.last_name,
        middle_name=user.fullname.middle_name,
        deleted_at=user.deleted_at.value,
        version=user.version,
    )


#
# await self._session.execute(
#     text(
#         """
#         INSERT INTO user (id, username, first_name, last_name, middle_name, deleted_at, version)
#         VALUES (:id, :username, :first_name, :last_name, :middle_name, :deleted_at, :version)
#         """
#     ),
#     c.convert_user_entity_to_db_model(user),
# )
