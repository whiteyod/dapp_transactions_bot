from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database.db import get_all_dapps, get_transactions_for_dapp
from keyboards import cancel_kb, saved_kb, main_dapps_menu_kb


router = Router()


@router.callback_query(F.data == "show_dapps")
async def show_all_dapps(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    rows = await get_all_dapps(user_id)
    items = []
    # Get dapps info and store as a list of dicts
    for app_name, owner, treasury in rows:
        
        # balance = sum(transactions)
        items.append({
            "name": app_name,
            "owner": owner,
            "treasury": treasury,
        })
    # Get transactions info, sum it and append to items
    trans_rows = [
        await get_transactions_for_dapp(user_id, it["name"]) for it in items
    ]
    for i, trans in enumerate(trans_rows):
        balance = sum(t[0] for t in trans) if trans else 0.0
        items[i]["balance"] = balance
    # Create message layout
    daaps_message = ["<b>.................</b>"]
    for it in items:
        daaps_message.append(
            f"{it["name"]} > Balance: {it["balance"]}\n"
            f"Owner: {it["owner"]}\n"
            f"Treasury: {it["treasury"]}"
        )
    edited_message = '\n'.join(daaps_message)
    await callback.message.answer(f"{edited_message}", reply_markup=main_dapps_menu_kb())

