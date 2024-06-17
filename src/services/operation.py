import os
import re
from datetime import datetime

from dotenv import load_dotenv
from openai import AsyncOpenAI

from src.database.database import get_session
from src.database.models import Category, Operation, ShopCategory
from src.repository.operation import (
    add_unsorted_operation,
    get_unsorted_operation_by_shop_user_id,
    get_unsorted_payment, get_unsorted_payment_by_id, get_unsorted_payment_count,
)
from src.repository.shop_matching import add_shop_matching, get_category_by_shop
from src.repository.user import get_user_by_tg_user_id
from src.schemas.android_app import NotificationData


async def parse_notification(data: NotificationData, user_id: int) -> None:
    async with get_session() as session:
        match = re.match(r"([A-Z]{3})(\d+\.\d{2}) with ([^\s]+) •••• (\d{4})", data.text)
        if match:
            category_id = await get_category_by_shop(session, data.title, user_id)
            print(category_id)
            await add_unsorted_operation(
                session,
                Operation(
                    owner_id=user_id,
                    shop=data.title,
                    time=datetime.now(),
                    currency=match.group(1),
                    amount=int(float(match.group(2)) * 100),
                    card=match.group(4) + match.group(3),
                    category_id=category_id,
                ),
            )


async def get_unsorted_payment_by_tg_id(tg_user_id: int) -> Operation | None:
    async with get_session() as session:
        user = await get_user_by_tg_user_id(session, tg_user_id)
        return await get_unsorted_payment(session, user.id)


async def get_suggestion_for_unsorted_payment(shop_name: str, options: list[Category]) -> str:
    category_names = [category.name for category in options]
    prompt = (
        f"Shop name: {shop_name}\n"
        f"Categories: {', '.join(category_names)}\n"
        f"Predict the most appropriate category for the shop name from the given categories.You can return only value "
        f"what i send to you"
    )
    load_dotenv()
    client = AsyncOpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    try:
        chat_completion = await client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-3.5-turbo",
        )

        return chat_completion.choices[0].message.content

    except Exception as e:
        print(f"An error occurred: {e}")
        return "Error"


async def set_match_shop_category(shop_name: str, owner_id: int, category_id: int) -> int:
    async with get_session() as session:
        counter = 0
        unsorted_operations = await get_unsorted_operation_by_shop_user_id(session, owner_id, shop_name)
        await add_shop_matching(
            session,
            ShopCategory(
                shop_name=shop_name,
                category_id=category_id,
                owner_id=owner_id,
            ),
        )
        for operation in unsorted_operations:
            counter += 1
            operation.category_id = category_id
    return counter


async def set_operation_category(operation_id: int, category_id: int) -> None:
    async with get_session() as session:
        payment = await get_unsorted_payment_by_id(session, operation_id)
        if payment:
            payment.category_id = category_id


async def sort_operation(user, user_data: dict) -> str:
    if user.payment_mode == "remember":
        counter = await set_match_shop_category(user_data["shop"], user.id, user_data["category_id"])
        return f"{counter} operations was moved"
    else:
        await set_operation_category(user_data["unsorted_payment_id"], user_data["category_id"])
        return f"Operation was moved"


async def get_unsorted_payments_count(tg_user_id: int) -> int:
    async with get_session() as session:
        user = await get_user_by_tg_user_id(session, tg_user_id)
        if user:
            return await get_unsorted_payment_count(session, user.id)
        return 0
