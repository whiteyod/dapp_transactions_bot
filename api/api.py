from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from api.auth_verification import verify_telegram_auth
from database.db import get_all_dapps, save_dapp_data_in_db, \
    save_transaction_in_db, get_transactions_sum, get_transactions_for_dapp, \
    delete_dapp_from_db, delete_transactions_from_db


app = FastAPI()


# Create dApp pydantic models
class CreateDAppPayload(BaseModel):
    name: str
    owner: str
    treasury: str


class TransactionPayload(BaseModel):
    trans_amount: float
    timestamp: str | None = None
    description: str | None = None


# Enable middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://dapptransactionsmini.vercel.app",
        "https://dapptrans.mini.app.lolkek.live"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# ------------------------ API Endpoints ---------------------

# Get all user dApps data
@app.get("/dapps")
async def get_dapps(user_id: int = Depends(verify_telegram_auth)):
    rows = await get_transactions_sum(user_id=user_id)

    return [
        {
            "id": item["name"],
            "name": item["name"],
            "ownerWallet": item["owner"],
            "treasuryWallet": item["treasury"],
            "balance": float(item["balance"]),
            "usdBalance": float(item["USD"])
        }
        for item in rows
    ]


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
    rows = await get_transactions_sum(user_id=user_id)
    for item in rows:
        if item["name"] == app_name:
            return {
                "id": item["name"],
                "name": item["name"],
                "ownerWallet": item["owner"],
                "treasuryWallet": item["treasury"],
                "balance": float(item["balance"]),
                "usdBalance": float(item["USD"])
            }
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

    return {"message": f"Transaction saved for {app_name}"}


# Remove dApp
@app.delete("/dapps/{app_name}")
async def delete_dapp(
    app_name: str, user_id: int = Depends(verify_telegram_auth)
):
    await delete_dapp_from_db(user_id=user_id, app_name=app_name)
    await delete_transactions_from_db(user_id=user_id, app_name=app_name)

    return {"message": f"dApp {app_name} deleted"}
    




