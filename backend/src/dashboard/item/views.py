import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from dashboard.auth import dependencies
from dashboard.auth.models import User
from dashboard.database import get_session
from dashboard.item import service
from dashboard.item.models import ItemCreate, ItemDelete, ItemRead, ItemUpdate

router = APIRouter(prefix="/items", tags=["items"])


@router.get(
    "/",
    response_model=list[ItemRead],
    summary="List all items",
    description="Returns all items. Requires authentication.",
)
async def get_items(
    current_user: User = Depends(dependencies.get_current_user),
    session: AsyncSession = Depends(get_session),
):
    return await service.get_items(session=session)


@router.get(
    "/{item_id}",
    response_model=ItemRead,
    summary="Get an item",
    description="Returns a single item by ID. Requires authentication.",
)
async def get_item(
    item_id: uuid.UUID,
    current_user: User = Depends(dependencies.get_current_user),
    session: AsyncSession = Depends(get_session),
):
    item = await service.get_item(item_id=item_id, session=session)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.post(
    "/",
    response_model=ItemRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create an item",
    description="Creates a new item. Requires authentication.",
)
async def create_item(
    item_in: ItemCreate,
    current_user: User = Depends(dependencies.get_current_user),
    session: AsyncSession = Depends(get_session),
):
    return await service.create_item(item_in=item_in, session=session)


@router.put(
    "/{item_id}",
    response_model=ItemRead,
    summary="Update an item",
    description="Updates an existing item by ID. Requires authentication.",
)
async def update_item(
    item_id: uuid.UUID,
    item_in: ItemUpdate,
    current_user: User = Depends(dependencies.get_current_user),
    session: AsyncSession = Depends(get_session),
):
    item = await service.update_item(item_id=item_id, item_in=item_in, session=session)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.delete(
    "/{item_id}",
    response_model=ItemDelete,
    summary="Delete an item",
    description="Deletes an item by ID and returns the deleted item. Requires authentication.",
)
async def delete_item(
    item_id: uuid.UUID,
    current_user: User = Depends(dependencies.get_current_user),
    session: AsyncSession = Depends(get_session),
):
    item = await service.delete_item(item_id=item_id, session=session)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item
