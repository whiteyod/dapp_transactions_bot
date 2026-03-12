from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database.db import get_dapp_names, save_transaction_in_db
from keyboards import cancel_transaction_kb, select_dapp_kb, start_kb


router = Router()


class AddTransaction(StatesGroup):
    app_name = State()
    transaction_amount = State()


# Add transaction handler
@router.callback_query(F.data == "add_transaction")
async def select_dapp_for_transaction(
    callback: types.CallbackQuery,
    state: FSMContext
):
    user_id = callback.from_user.id
    app_names = await get_dapp_names(user_id=user_id)
    await state.set_state(AddTransaction.app_name)
    await callback.message.edit_text(
        "Select dApp:",
        reply_markup=select_dapp_kb(app_names=app_names)
    )


# Selected dApp hanlder
@router.callback_query(F.data.startswith("app_"))
async def add_transaction(
    callback: types.CallbackQuery,
    state: FSMContext
):
    app_name = callback.data.replace("app_", "")
    await state.update_data(app_name=app_name)
    await state.set_state(AddTransaction.transaction_amount)
    await callback.message.edit_text(
        f"Selected dApp: <b>{app_name}</b>\n\nEnter transaction amount in SOL:",
        reply_markup=cancel_transaction_kb()
    )


# Save transaction data handler
@router.message(AddTransaction.transaction_amount)
async def save_transaction_data(
    message: types.Message,
    state: FSMContext
):
    user_id = message.from_user.id
    await state.update_data(transaction_amount=message.text)
    data = await state.get_data()
    trans_amount = data["transaction_amount"]
    app_name = data["app_name"]

    await save_transaction_in_db(
        user_id=user_id, app_name=app_name, trsansaction_amount=trans_amount
    )
    await message.answer(
        f"Transaction for <b>{app_name}</b> saved. \n\nWhat next?",
        reply_markup=start_kb()
    )


    
    

