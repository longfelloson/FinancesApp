from typing import List, Optional

from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from operations.models import Operation
from operations.schemas import CreateOperation


async def create_operation(
    operation: CreateOperation,
    session: AsyncSession,
) -> Operation:
    await session.execute(insert(Operation).values(
        name=operation.name, amount=operation.amount, type_=operation.type_)
    )
    await session.commit()


async def get_operation(operation_id: str, session: AsyncSession) -> Optional[Operation]:
    operation = await session.execute(select(Operation).where(Operation.id_ == operation_id))
    return operation.scalar_one_or_none()


async def get_operations(
    session: AsyncSession,
    limit: int,
    offset: int,
    **options,
) -> List[Operation]:
    """Get all operations by provided options"""
    stmt = select(Operation).limit(limit).offset(offset)
    if options:
        stmt = stmt.filter_by(**options)

    operations = await session.execute(stmt)
    return operations.scalars().all()


async def update_operation(
    operation_id: str,
    session: AsyncSession,
    **values,
):
    await session.execute(update(Operation).where(Operation.id_ == operation_id).values(**values))
    await session.commit()


async def delete_operation(operation_id: str, session: AsyncSession):
    await session.execute(delete(Operation).where(Operation.id_ == operation_id))
    await session.commit()
