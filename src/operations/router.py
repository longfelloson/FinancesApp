from typing import List

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
)
from fastapi.responses import (
    JSONResponse,
    HTMLResponse,
)
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import (
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED,
)

from auth.token import verify_access_token
from database import get_async_session
from operations import crud
from operations.enums import OperationType
from operations.schemas import (
    Operation,
    CreateOperation,
)

router = APIRouter(tags=['Operations'], dependencies=[Depends(verify_access_token)])
templates = Jinja2Templates(directory='../templates/operations')


@router.get("/operations", status_code=HTTP_200_OK, response_model=List[Operation])
async def get_operations(
    limit: int = 10,
    offset: int = 0,
    session: AsyncSession = Depends(get_async_session)
):
    """Return all operations by provided options"""
    operations = await crud.get_operations(session, limit=limit, offset=offset)
    return operations


@router.get("/operations/{operation_id}", status_code=HTTP_200_OK, response_model=Operation)
async def get_operation(operation_id: int, session: AsyncSession = Depends(get_async_session)):
    """Return operation by provided id"""
    operation = await crud.get_operation(operation_id, session)
    if not operation:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail={"msg": "A user with this id does not exist."},
        )

    return operation


@router.post("/operations", status_code=HTTP_201_CREATED, response_class=JSONResponse)
async def create_operation(operation: CreateOperation, session: AsyncSession = Depends(get_async_session)):
    """Create a new operation"""
    operation.type_ = OperationType.EXPENSE if operation.amount < 0 else OperationType.INCOME

    await crud.create_operation(operation, session)

    return JSONResponse(status_code=HTTP_201_CREATED, content={"msg": "Operation created."})


@router.delete("/operations", status_code=HTTP_200_OK, response_class=JSONResponse)
async def delete_operation(operation_id: int, session: AsyncSession = Depends(get_async_session)):
    """Delete operation by provided id"""
    await crud.delete_operation(operation_id, session)

    return JSONResponse(status_code=HTTP_200_OK, content={"msg": "Operation deleted."})


@router.get("/create-operation", status_code=HTTP_200_OK, response_class=HTMLResponse)
async def get_create_operation_page(request: Request):
    """Return HTML page with form to create an operation"""
    return templates.TemplateResponse("create-operation.html", {"request": request})
