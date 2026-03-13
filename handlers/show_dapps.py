from aiogram import F, Router, types

from database.db import get_all_dapps, get_transactions_for_dapp
from keyboards import main_dapps_menu_kb
from services.container import get_quotes


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
    # Get current SOL price
    symbol = "SOL"
    quotes = await get_quotes([symbol])
    result = quotes.get(symbol.upper())
    for i, trans in enumerate(trans_rows):
        balance = sum(t[0] for t in trans) if trans else 0.0
        items[i]["balance"] = balance
        items[i]["USD"] = balance * result
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

