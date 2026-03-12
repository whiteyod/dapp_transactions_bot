"""Command handlers (e.g. /start, /help).

Aiogram uses routers to group handlers by feature.
This module contains handlers triggered by text commands.
"""
 
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
 
from keyboards import start_kb
from database.db import create_all_tables
 
 
# Router instance exported and included in `main.py`.
router = Router()
 
 
@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    """Handle `/start`.

    This is typically the first message users see. Customize it to introduce
    your bot, show main menu buttons, etc.
    """
    await create_all_tables()
 
    await message.answer(
        "Add transaction, see your dApps or add a new one.",
        reply_markup=start_kb(),
    )