from pydantic import BaseModel


class CreateChatRequestSchema(BaseModel):
    user_id: str | None
    username: str
    first_name: str
    last_name: str
    middle_name: str | None


class GetAllUsersSchema(BaseModel): ...
