from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from keyboards import start_kb


router = Router()

@router.callback_query(F.data == 'cancel')
async def cancel_button(
    callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
            "Add transaction, see your dApps or add a new one.",
            reply_markup=start_kb(),
        )