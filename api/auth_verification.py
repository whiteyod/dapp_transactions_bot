import json
import hmac
import hashlib
from urllib.parse import parse_qsl
from fastapi import HTTPException, Query

from config_reader import config


BOT_TOKEN = config.bot_token.get_secret_value()


def verify_telegram_auth(init_data: str = Query(..., alias="init_data")) -> int:
    """ Verify user credentilas to login. """
    parsed_data = dict(parse_qsl(init_data, keep_blank_values=True))
    received_hash = parsed_data.pop("hash", None)

    if not received_hash:
        raise HTTPException(status_code=401, detail="Missing Telegram hash")
    
    data_check_string = "\n".join(
        f"{key}={value}" for key, value in sorted(parsed_data.items())
    )

    secret_key = hmac.new(
        key=b"WebAppData",
        msg=BOT_TOKEN.encode(),
        digestmod=hashlib.sha256,
    ).hexdigest()

    calculated_hash = hmac.new(
        key=secret_key,
        msg=data_check_string.encode(),
        digestmod=haslib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(calculated_hash, received_hash):
        raise HTTPException(status_code=401, detail="Invalid Telegram auth")

    user_raw = parsed_data.get("user")
    if not user_raw:
        raise HTTPException(status_code=401, detail="Missing Telegram user")

    user = json.loads(user_raw)
    user_id = user.get("id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid Telegram use")

    return int(user_id)