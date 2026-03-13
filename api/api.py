import requests
from fastapi import FastAPI, HTTPException, Depends, Query
from pydantic import BaseModel

from config_reader import config
from database.db import get_all_dapps, save_dapp_data_in_db, \
    save_transaction_in_db, get_transactions_sum, get_transactions_for_dapp, \
    delete_dapp_from_db, delete_transactions_from_db


app = FastAPI()


# Get bot credentials
BOT_TOKEN = config.bot_token.get_secret_value()


# Verify user credentials to login
def verify_telegram_auth(init_data: str = Query(...)) -> int:
    """ Verify initData with Telegram and return user_id. """
    response = requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/verifyInitData",
        data={"initData": init_data}
    )
    # Check initData, raise error if failed
    if not response.ok:
        raise HTTPException(
            status_code=401, detail="Invalid auth"
        )
    # Return user_id from verified data
    data = response.json()
    return data.get("user", {}).get("id")


# Create dApp pydantic models
class CreateDAppPayload(BaseModel):
    name: str
    owner: str
    treasury: str


class TransactionPayload(BaseModel):
    app_name: str
    trans_amount: float


# ------------------------ API Endpoints ---------------------

# Get all user dApps data
@app.get("/dapps")
async def get_dapps(user_id: int = Depends(verify_telegram_auth)):
    rows = await get_all_dapps(user_id=user_id)

    return [{"name": r[0], "owner": r[1], "treasury": r[2]} for r in rows]


# Return raw transaction rows
@app.get("/dapps/{app_name}/transactions")
async def get_transactions_fror_dapp_endpoint(
    app_name: str, user_id: int = Depends(verify_telegram_auth)
):
    trans = await get_transactions_for_dapp(
        user_id=user_id, app_name=app_name
    )
    
    return [{"amount": t[0], "timestamp": t[1]} for t in trans]


# Get one user dApp data
@app.get("/dapps/{app_name}")
async def get_dapp(
    app_name: str, user_id: int = Depends(verify_telegram_auth)
):
    rows = await get_all_dapps(user_id=user_id)
    for r in rows:
        if r[0] == app_name:
            return {"name": r[0], "owner": r[1], "treasury": r[2]}
    raise HTTPException(status_code=404, detail="dApp not found")


# Create new dApp endpoint
@app.post("/dapps")
async def create_dapp(
    payload: CreateDAppPayload, user_id: int = Depends(verify_telegram_auth)
):
    await save_dapp_data_in_db(
        user_id=user_id,
        app_name=payload.name,
        wallet_owner=payload.owner,
        wallet_treasury=payload.treasury
    )

    return {"message": "dApp created"}


# Add new transaction for dApp
@app.post("/dapps/{app_name}/transactions")
async def add_transaction(
    app_name: str,
    payload: TransactionPayload,
    user_id: int = Depends(verify_telegram_auth)
):
    await save_transaction_in_db(
        user_id=user_id,
        app_name=app_name,
        trsansaction_amount=payload.trans_amount
    )

    return {"message": f"Transaction saved for {payload.app_name}"}


# Remove dApp
@app.delete("/dapps/{app_name}")
async def delete_dapp(
    app_name: str, user_id: int = Depends(verify_telegram_auth)
):
    await delete_dapp_from_db(user_id=user_id, app_name=app_name)
    await delete_transactions_from_db(user_id=user_id, app_name=app_name)

    return {"message": f"dApp {app_name} deleted"}
    




