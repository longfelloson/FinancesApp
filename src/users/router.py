from fastapi import APIRouter
from starlette.responses import JSONResponse

from auth.utils import CurrentUser
from database import AsyncSession
from users import crud
from users.schemas import UpdateBalance

router = APIRouter(tags=["Users"])


@router.get("/user-balance", response_class=JSONResponse)
async def get_user_balance(user: CurrentUser, session: AsyncSession):
    """Get user balance."""
    user_balance = await crud.get_user_balance(user.id_, session)

    return JSONResponse({"balance": user_balance})


@router.put("/user-balance", response_class=JSONResponse)
async def update_user_balance(
    data: UpdateBalance,
    user: CurrentUser,
    session: AsyncSession
):
    """Update user balance."""
    await crud.update_user_balance(user.id_, data, session)

    return JSONResponse({"msg": "User balance updated"})
