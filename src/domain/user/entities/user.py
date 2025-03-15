from domain.base.entity.aggregate import AggregateRoot
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

from dataclasses import dataclass, field
from typing import Self


@dataclass
class User(AggregateRoot):
    id: UserId
    username: Username
    fullname: FullName
    deleted_at: DeletedAt = field(
        default_factory=lambda: DeletedAt.not_deleted(), kw_only=True
    )
    version: int = field(default=0, kw_only=True)

    @classmethod
    def create(
        cls,
        user_id: UserId,
        username: Username,
        fullname: FullName,
    ) -> Self:

        user = User(user_id, username, fullname)
        user.register_event(
            UserCreated(
                user_id=user_id.to_raw(),
                username=username.to_raw(),
            )
        )
        return user

    def set_username(self, username: Username) -> None:
        self._is_not_deleted()

        if username != self.username:
            self.username = username
            self._version_upgrade()
            self.register_event(
                UsernameUpdated(
                    user_id=self.id.to_raw(),
                    username=username.to_raw(),
                )
            )

    def set_fullname(self, fullname: FullName) -> None:
        self._is_not_deleted()

        if fullname != self.fullname:
            self.fullname = fullname
            self._version_upgrade()

            # Only register internal event for event consistency, but not send it.
            self.register_event(
                FullnameUpdated(
                    user_id=self.id.to_raw(),
                    first_name=fullname.first_name,
                    last_name=fullname.last_name,
                    middle_name=fullname.middle_name,
                )
            )

    def delete(self) -> None:
        if not self.deleted_at.is_deleted():
            self.deleted_at = DeletedAt.deleted_at()
            self._version_upgrade()
            self.register_event(UserDeleted(user_id=self.id.to_raw()))

    def restore(self) -> None:
        if self.deleted_at.is_deleted():
            self.deleted_at = DeletedAt.not_deleted()
            self._version_upgrade()
            self.register_event(UserRestored(user_id=self.id.to_raw()))

    def _is_not_deleted(self):
        if self.deleted_at.is_deleted():
            raise UserIsDeletedException(user_id=self.id.to_raw())

    def _version_upgrade(self) -> None:
        self.version += 1
