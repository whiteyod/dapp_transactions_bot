"""Keyboard builders.

Keep keyboard creation in a separate module so handlers stay small and readable.
This also makes it easier to reuse the same keyboards across multiple handlers.
"""
 
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
 
 
def start_kb() -> types.InlineKeyboardMarkup:
    """Create a one-button inline keyboard.

    The `callback_data` value must match the filter used in the callback handler
    (see `handlers/buttons.py`).
    """
 
    # InlineKeyboardBuilder helps you add buttons and then convert to markup.
    kb = InlineKeyboardBuilder()
 
    # Add a single inline button.
    kb.add(
        types.InlineKeyboardButton(
            text="See dApps",
            callback_data="show_dapps"
        ),
        types.InlineKeyboardButton(
            text="Add new dApp",
            callback_data="add_app",
        ),
        types.InlineKeyboardButton(
            text="Add Transaction",
            callback_data="add_transaction"
        )
    )
    kb.adjust(1)
 
    # Convert builder to markup object expected by `reply_markup=test_button_kb()`.
    return kb.as_markup()


def select_dapp_kb(app_names: list):
    kb = InlineKeyboardBuilder()
    for i in app_names:
        kb.add(
            types.InlineKeyboardButton(
                text=f"{i}",
                callback_data=f"app_{i}"
            )
        )
    kb.add(
        types.InlineKeyboardButton(
            text="Cancel",
            callback_data="cancel"
        )
    )
    kb.adjust(1)

    return kb.as_markup()


def delete_dapp_kb(app_names: list):
    kb = InlineKeyboardBuilder()
    for i in app_names:
        kb.add(
            types.InlineKeyboardButton(
                text=f"{i}",
                callback_data=f"delete_app_{i}"
            )
        )
    kb.add(
        types.InlineKeyboardButton(
            text="Cancel",
            callback_data="cancel"
        )
    )
    kb.adjust(1)

    return kb.as_markup()


def see_transactions_kb(app_names: list):
    kb = InlineKeyboardBuilder()
    for i in app_names:
        kb.add(
            types.InlineKeyboardButton(
                text=f"{i}",
                callback_data=f"see_{i}"
            )
        )
    kb.add(
        types.InlineKeyboardButton(
            text="Cancel",
            callback_data="cancel"
        )
    )
    kb.adjust(1)

    return kb.as_markup()


# Delete dApp confirmation keyboard
def confirm_delete_kb(app_name: str):
    kb = InlineKeyboardBuilder()
    kb.add(
        types.InlineKeyboardButton(
            text=f"DELETE {app_name}",
            callback_data="remove_dapp"
        ),
        types.InlineKeyboardButton(
            text="Cancel",
            callback_data="delete_dapp"
        )
    )

    return kb.as_markup()


# dApp main menu keyboards
def main_dapps_menu_kb():
    kb = InlineKeyboardBuilder()
    kb.add(
        types.InlineKeyboardButton(
            text="Transactions",
            callback_data="see_transactions"
        ),
        types.InlineKeyboardButton(
            text="Delete dApp",
            callback_data="delete_dapp"
        ),
        types.InlineKeyboardButton(
            text="Back",
            callback_data="cancel"
        )
    )
    kb.adjust(1)

    return kb.as_markup()


def cancel_transaction_kb():
    kb = InlineKeyboardBuilder()
    kb.add(
        types.InlineKeyboardButton(
            text="Cancel",
            callback_data="add_transaction"
        )
    )

    return kb.as_markup()


def cancel_kb() -> types.InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(
        types.InlineKeyboardButton(
            text="Cancel",
            callback_data="cancel"
        )
    )

    return kb.as_markup()


def back_to_see_transactions_kb() -> types.InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(
        types.InlineKeyboardButton(
            text="Back",
            callback_data="see_transactions"
        )
    )

    return kb.as_markup()