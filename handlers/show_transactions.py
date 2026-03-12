from aiogram import F, Router, types

from database.db import get_all_dapps, get_transactions_for_dapp, get_dapp_names
from keyboards import main_dapps_menu_kb, see_transactions_kb,\
    back_to_see_transactions_kb


router = Router()


# See transaction by dApp handler
@router.callback_query(F.data == "see_transactions")
async def see_transactions_by_app(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    names = await get_dapp_names(user_id=user_id)
    await callback.message.edit_text(
        "Select dApp to see transactions:",
        reply_markup=see_transactions_kb(names)
    )


@router.callback_query(F.data.startswith("see_"))
async def select_dapp_to_see(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    app_name = callback.data.replace("see_", "")

    trans_rows = await get_transactions_for_dapp(user_id=user_id, app_name=app_name)
    items = []
    for i, trans in enumerate(trans_rows):
        items.append(
            f"{trans[0]} SOL\n")
    print([i for i in items])
    formatted = "\n".join(items)
    await callback.message.edit_text(
        f"{formatted}", reply_markup=back_to_see_transactions_kb()
    )