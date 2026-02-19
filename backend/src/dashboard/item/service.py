import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dashboard.item.models import Item, ItemCreate, ItemUpdate


async def get_items(*, session: AsyncSession) -> list[Item]:
    result = await session.scalars(select(Item))
    return list(result.all())


async def get_item(*, item_id: uuid.UUID, session: AsyncSession) -> Item | None:
    return await session.scalar(select(Item).where(Item.id == item_id))


async def create_item(*, item_in: ItemCreate, session: AsyncSession) -> Item:
    item = Item(title=item_in.title, description=item_in.description)
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item


async def update_item(
    *, item_id: uuid.UUID, item_in: ItemUpdate, session: AsyncSession
) -> Item | None:
    item = await get_item(item_id=item_id, session=session)
    if item is None:
        return None
    if item_in.title is not None:
        item.title = item_in.title
    if item_in.description is not None:
        item.description = item_in.description
    await session.commit()
    await session.refresh(item)
    return item


async def delete_item(*, item_id: uuid.UUID, session: AsyncSession) -> Item | None:
    item = await get_item(item_id=item_id, session=session)
    if item is None:
        return None
    await session.delete(item)
    await session.commit()
    return item
