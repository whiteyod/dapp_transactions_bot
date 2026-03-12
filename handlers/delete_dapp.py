from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database.db import delete_dapp_from_db, delete_transactions_from_db,\
    get_dapp_names
from keyboards import cancel_kb, saved_kb, start_kb, delete_dapp_kb,\
    confirm_delete_kb


router = Router()

class DeleteDapp(StatesGroup):
    app_name = State()
    confirm_delete = State()



@router.callback_query(F.data == "delete_dapp")
async def delete_dapp_handler(
    callback: types.CallbackQuery, state: FSMContext
):
    # Clear previous states
    await state.clear()
    # Get user_id and list of his dApp names
    user_id = callback.from_user.id
    names = await get_dapp_names(user_id)
    # Set state to store dApp name to be deleted
    await state.set_state(DeleteDapp.app_name)
    # Return a keyboard with dApp selection to delete
    await callback.message.edit_text(
        "Select dApp you want to delete:",
        reply_markup=delete_dapp_kb(names)
    )


@router.callback_query(F.data.startswith("delete_app_"))
async def delete_dapp_selected(
    callback: types.CallbackQuery, state: FSMContext
):
    # Get dApp name from callback nad store it in state
    app_name = callback.data.replace("delete_app_", "")
    await state.update_data(app_name=app_name)
    # Set state to catch delete confirmation
    await state.set_state(DeleteDapp.confirm_delete)
    await callback.message.edit_text(
        f"You trying to delete {app_name}\n\nAre you sure?",
        reply_markup=confirm_delete_kb(app_name)
    )


@router.callback_query(F.data == "remove_dapp")
async def remove_dapp(
    callback: types.CallbackQuery, state: FSMContext
):
    user_id = callback.from_user.id
    # Get dApp name to be deleted
    data = await state.get_data()
    app_name = data["app_name"]
    # Remove dApp data from the DBs
    await delete_dapp_from_db(user_id=user_id, app_name=app_name)
    await delete_transactions_from_db(user_id=user_id, app_name=app_name)
    # Inform user about successfull deleteion
    await callback.message.edit_text(
        f"dApp {app_name} has been removed",
        reply_markup=start_kb()
    )

