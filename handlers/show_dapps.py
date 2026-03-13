from aiogram import F, Router, types

from database.db import get_all_dapps, get_transactions_for_dapp, get_transactions_sum
from keyboards import main_dapps_menu_kb
from services.container import get_quotes


router = Router()


@router.callback_query(F.data == "show_dapps")
async def show_all_dapps(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    items = await get_transactions_sum(user_id=user_id)
    # Create message layout
    daaps_message = ["<b>.................</b>\n\n"]
    for it in items:
        daaps_message.append(
            f"<b>{it["name"]}</b>\n"
            f"{it["balance"]} SOL ({it["USD"]:.2f} USD)\n"
            f"<b>Owner:</b> {it["owner"]}\n"
            f"<b>Treasury:</b> {it["treasury"]}\n\n"
            "<b>.................</b>\n"
        )
    edited_message = '\n'.join(daaps_message)
    await callback.message.edit_text(f"{edited_message}", reply_markup=main_dapps_menu_kb())

