from operator import and_
from typing import Optional, Union

from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from users.models import User
from users.schemas import UserCredentials, UpdateBalance


async def create_user(user: UserCredentials, session: AsyncSession) -> None:
    await session.execute(insert(User).values(**user.model_dump()))
    await session.commit()


async def get_user_by_id(user_id: int, session: AsyncSession) -> Optional[User]:
    user = await session.execute(select(User).where(User.id_ == user_id))
    return user.scalar_one_or_none()


async def get_user_by_email(email: str, session: AsyncSession) -> Optional[User]:
    user = await session.execute(select(User).where(User.email == email))
    return user.scalar_one_or_none()


async def get_user_by_credentials(credentials: UserCredentials, session: AsyncSession) -> Optional[User]:
    user = await session.execute(select(User).where(and_(
        User.email == credentials.email, User.hashed_password == credentials.hashed_password
    )))
    return user.scalar_one_or_none()


async def update_user_balance(
    user_id: int,
    data: UpdateBalance,
    session: AsyncSession,
) -> None:
    """If amount > 0 increase user's balance otherwise decrease user's balance.'"""
    stmt = (
        update(User)
        .where(User.id_ == user_id)
        .values(balance=User.balance + data.amount if data.amount > 0 else User.balance - abs(data.amount))
    )
    await session.execute(stmt)
    await session.commit()


async def get_user_balance(user_id: int, session: AsyncSession) -> Union[int, float]:
    user_balance = await session.execute(select(User.balance).where(User.id_ == user_id))
    return user_balance.scalar_one()
