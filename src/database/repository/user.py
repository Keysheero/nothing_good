from sqlalchemy import select, Row, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from .abstract import Repository
from ..models.base import BaseModel
from ..models.user import User


class UserRepository(Repository[User]):

    def __init__(self, session: AsyncSession):
        super().__init__(type_model=User, session=session)

    async def new(self, user_id, chat_id, user_name):
        await self.session.merge(
            self.type_model(user_id=user_id,
                            chat_id=chat_id,
                            user_name=user_name)
        )

    async def check_user(self, user_id) -> Row or None:
        statement = select(self.type_model).where(self.type_model.user_id == user_id)
        return (await self.session.execute(statement)).one_or_none()

    async def get_many(
            self, whereclause, limit: int = 100, order_by=None
    ) -> Sequence[BaseModel]:
        """Get many models from the database with whereclause.

        :param whereclause: Where clause for finding models
        :param limit: (Optional) Limit count of results
        :param order_by: (Optional) Order by clause.

        Example:
        >> Repository.get_many(Model.id == 1, limit=10, order_by=Model.id)

        :return: List of founded models
        """
        statement = select(self.type_model).where(whereclause).limit(limit)
        if order_by:
            statement = statement.order_by(order_by)

        return (await self.session.scalars(statement)).all()

    async def get_all(self, order_by=None) -> Sequence[BaseModel]:
        statement = select(self.type_model)
        if order_by:
            statement = statement.order_by(order_by)
        result = await self.session.execute(statement)
        return [user_id for (user_id,) in result.all()]
