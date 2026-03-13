"""Bot entrypoint.

This module wires together:
- configuration (token loading)
- dispatcher + storage (FSM)
- routers (handlers)

Typical customization points for your own template-based bot:
- add more routers in `dp.include_routers(...)`
- swap `MemoryStorage()` for Redis storage in production
- configure logging level/format
- custom logging setup with the `logger` library (optional; aiogram provides good logging by default)
"""

import asyncio
import logging
import uvicorn

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from loguru import logger

from api.api import app
from config_reader import config
from handlers import add_transactions, commands, create_dapp, show_dapps, \
    another_buttons, delete_dapp, show_transactions

# Basic logging so you can see incoming updates and errors in the console.
logging.basicConfig(level=logging.INFO)

# FSM storage keeps per-user/per-chat state for multi-step dialogs.
# `MemoryStorage` is fine for local development, but it resets on every restart.
storage = MemoryStorage()

async def main() -> None:
    """Start the bot using long polling.

Long polling is the simplest way to run a bot locally.
If you deploy via webhooks, remove `start_polling(...)` and configure webhook.
"""

    # Create bot client with the token loaded from `.env` (see `config_reader.py`).
    bot = Bot(
        token=config.bot_token.get_secret_value(),
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        ))

    # Dispatcher is the main routing engine: it receives updates and passes them
    # to the first handler that matches filters.
    dp = Dispatcher(storage=storage)

    # Attach routers with handlers.
    # Add your own routers here (e.g. `dp.include_routers(admin.router, ...)`).
    dp.include_routers(
        commands.router, 
        create_dapp.router,
        add_transactions.router,
        show_dapps.router,
        another_buttons.router,
        delete_dapp.router,
        show_transactions.router
    )

    # If the bot previously worked in webhook mode, remove webhook and optionally
    # drop pending updates so you start from a clean state.
    await bot.delete_webhook(drop_pending_updates=True)

    # Init API for mini app
    config_api = uvicorn.Config(app, host="127.0.0.1", port=8020)
    server = uvicorn.Server(config_api)

    # Start bot and API for mini app.
    await asyncio.gather(dp.start_polling(bot), server.serve())


if __name__ == "__main__":
    # Log the bot's startup.
    logger.info(f'Your bot is running!')
    # `asyncio.run` creates an event loop, runs `main()`, and closes the loop.
    asyncio.run(main())
    # Log the bot's shutdown.
    logger.info(f'Your bot is shutting down!')