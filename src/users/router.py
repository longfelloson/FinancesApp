from fastapi import APIRouter, Depends, Request
from starlette.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from auth.utils import CurrentUser, get_current_user
from database import get_async_session
from users import crud
from users.models import User
from users.schemas import UpdateBalance

router = APIRouter(tags=["Users"])


@router.get("/balance", response_class=JSONResponse)
async def get_user_balance(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
):
    """Get user balance."""
    user = await get_current_user(request, session)
    user_balance = await crud.get_user_balance(user.id, session)

    return JSONResponse({"balance": user_balance})


@router.put("/balance", response_class=JSONResponse)
async def update_user_balance(
    request: Request,
    data: UpdateBalance,
    session: AsyncSession = Depends(get_async_session),
):
    """Update user balance."""
    user: User = await get_current_user(request, session)
    await crud.update_user_balance(user.id, data, session)

    return JSONResponse({"msg": "User balance updated"})
