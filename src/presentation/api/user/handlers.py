from fastapi import APIRouter, status, Depends, HTTPException
from dishka import AsyncContainer

from domain.base.exceptions.application import AppException
from application.dependency_injector.di import get_container
from application.mediator.mediator import Mediator
from application.user.commands.create_user import CreateUserCommand
from presentation.api.base_schemas import ErrorResponseSchema
from presentation.api.exception_builder import add_error_responses
from presentation.api.user.request import CreateChatRequestSchema
from presentation.api.user.response import CreateUserResponseSchema

user_router = APIRouter()


@user_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    description="Creates a new user and sends it in database. If username of user already exists, throws an Error",
    responses=add_error_responses(
        {status.HTTP_201_CREATED: {"model": CreateUserResponseSchema}},
    ),
)
async def create_user_handler(
    request: CreateChatRequestSchema, container: AsyncContainer = Depends(get_container)
):
    async with container() as c:
        mediator: Mediator = await c.get(Mediator)
        user, *_ = await mediator.handle_command(
            command=CreateUserCommand(
                user_id=request.user_id,
                username=request.username,
                first_name=request.first_name,
                last_name=request.last_name,
                middle_name=request.middle_name,
            )
        )

        return CreateUserResponseSchema.from_entity(user)
        # try:
        #     user, *_ = await mediator.handle_command(
        #         command=CreateUserCommand(
        #             user_id=request.user_id,
        #             username=request.username,
        #             first_name=request.first_name,
        #             last_name=request.last_name,
        #             middle_name=request.middle_name,
        #         )
        #     )
        # except AppException as e:
        #     raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=e.message)
        #
        # return CreateUserResponseSchema.from_entity(user)
