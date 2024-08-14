from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    status,
    Request,
)
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates

from auth.password import check_password, hash_password
from auth.token import create_access_token
from auth.schemas import AccessToken
from database import AsyncSession
from users import crud
from users.schemas import UserCredentials

router = APIRouter(tags=["Auth"])
templates = Jinja2Templates(directory="../templates/auth")


@router.post("/register", response_class=JSONResponse)
async def create_user(
    session: AsyncSession,
    credentials: OAuth2PasswordRequestForm = Depends(),
):
    user = await crud.get_user_by_email(credentials.username, session)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"msg": "User already exists."},
        )
    user_credentials = UserCredentials(
        email=credentials.username,
        hashed_password=hash_password(credentials.password)
    )

    await crud.create_user(user_credentials, session)

    token = create_access_token(user_credentials.email)
    return JSONResponse(
        content={"msg": "User created successfully.", "access_token": token.access_token},
        status_code=status.HTTP_201_CREATED
    )


@router.get("/register", response_class=HTMLResponse)
async def get_registration_page(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})


@router.post("/login", response_model=AccessToken)
async def login_user(
    session: AsyncSession,
    credentials: OAuth2PasswordRequestForm = Depends(),
):
    user = await crud.get_user_by_email(email=credentials.username, session=session)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"msg": "Invalid login."},
        )

    if not check_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"msg": "Invalid password."},
        )

    access_token = create_access_token(user.email)
    return access_token


@router.get("/login", response_class=HTMLResponse)
async def get_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})
