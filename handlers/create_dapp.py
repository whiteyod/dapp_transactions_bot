"""Callback query handlers (inline button clicks).

Inline keyboard buttons send a CallbackQuery update. You typically filter by
`callback_data` (see `keyboards.py`).
"""
 
from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database.db import save_dapp_data_in_db, save_transaction_in_db
from keyboards import cancel_kb, saved_kb, start_kb

 
 
# Router instance exported and included in `main.py`.
router = Router()
 

# Create an FSM object where data from user input will be stored.
class CreateDapp(StatesGroup):
    app_name = State()
    wallet_owner = State()
    wallet_treasury = State()


# Callback data handler for the `Test` button.
@router.callback_query(F.data == "add_app")
async def dapp_name_input(
    callback: types.CallbackQuery, state: FSMContext
) -> None:
    """Asks to enter name for new dApp."""
    await state.set_state(CreateDapp.app_name)
    await callback.message.answer(
        "Enter name for new dApp",
        reply_markup=cancel_kb()  # Shows a keyboard button for FSM testing.
    )


# Callback data handler for the `FSM test` button.
@router.message(CreateDapp.app_name)
async def dapp_wallet_owner_input(
    message: types.Message,
    state: FSMContext,
) -> None:
    """Handle presses of the "Test FSM" inline button.

    `state` is injected by aiogram and is useful for multi-step dialogs.
    Use it here, and keep it in the signature as a template.
    """
    # Save dApp name to the state
    await state.update_data(app_name=message.text)
    # Set the state to get data from the user.
    await state.set_state(CreateDapp.wallet_owner)
    # Ask the user to enter wallet owner
    await message.answer(
        'Enter wallet owner',
        reply_markup=cancel_kb()
    )


# Message handler for user input while the FSM is in the state
@router.message(CreateDapp.wallet_owner)
async def dapp_wallet_treasury_input(
    message: types.Message, state: FSMContext
):
    await state.update_data(wallet_owner=message.text)
    # We can use this data immediately, or use it later in other bot messages.
    await state.set_state(CreateDapp.wallet_treasury)
    await message.answer(
        "Enter wallet treasury (who will get the cash)",
        reply_markup=cancel_kb()
        )
    

@router.message(CreateDapp.wallet_treasury)
async def save_dapp_data(
    message: types.Message, state: FSMContext
):
    user_id = message.from_user.id
    await state.update_data(wallet_treasury=message.text)
    data = await state.get_data()
    dapp_name = data["app_name"]
    wallet_owner = data["wallet_owner"]
    wallet_treasury = data["wallet_treasury"]
    
    # Save dapp in the db
    await save_dapp_data_in_db(
        user_id=user_id, app_name=dapp_name,\
            wallet_owner=wallet_owner, wallet_treasury=wallet_treasury
    )
    await message.answer(
        "New dApp has been saved\n\nChoose what to do next",
        reply_markup=start_kb()
    )