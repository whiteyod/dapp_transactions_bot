import sqlite3
from services.container import get_quotes


# Creates database engine
conn = sqlite3.connect('assets.db')
c = conn.cursor()


# ------------------------------- Table Creation -------------------------

async def create_all_tables():
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS apps (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        app_name TEXT NOT NULL,
        wallet_owner TEXT NOT NULL,
        wallet_treasury TEXT NOT NULL
        )
    """)
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        app_name TEXT NOT NULL,
        transaction_amount REAL NOT NULL,
        timestamp TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()


# ----------------------------- Save Functions ----------------------------

async def save_dapp_data_in_db(
        user_id: int, app_name: str, wallet_owner: str, wallet_treasury: str
    ):
    c.execute(
        """
        INSERT INTO apps (user_id, app_name, wallet_owner, wallet_treasury)
        VALUES (?, ?, ?, ?)
        """, (user_id, app_name, wallet_owner, wallet_treasury)
    )
    conn.commit()


async def save_transaction_in_db(
        user_id: int, app_name: str, trsansaction_amount: float
):
    c.execute(
        """
        INSERT INTO transactions (user_id, app_name, transaction_amount)
        VALUES (?, ?, ?)
        """, (user_id, app_name, trsansaction_amount)
    )
    conn.commit()


# ------------------------------ Delete Functions -------------------------

async def delete_dapp_from_db(
        user_id: int, app_name: str
):
    c.execute(
        """
        DELETE FROM apps WHERE user_id = ? AND app_name = ?
        """, (user_id, app_name)
    )
    conn.commit()


async def delete_transactions_from_db(
        user_id: int, app_name: str
):
    c.execute(
        """
        DELETE FROM transactions WHERE user_id = ? AND app_name = ?
        """, (user_id, app_name)
    )
    conn.commit()


# --------------------------------- Get Data Functions -----------------------

async def get_all_dapps(user_id: int):
    c.execute(
        """
        SELECT app_name, wallet_owner, wallet_treasury
        FROM apps
        WHERE user_id = ?
        """, (user_id,)
    )

    return c.fetchall()


async def get_dapp_names(user_id: int):
    """ Return a list of dApp names converted to strings. """
    c.execute(
        """
        SELECT app_name
        FROM apps
        WHERE user_id = ?
        """, (user_id,)
    )
    result = c.fetchall()
    names = []
    for i in result:
        res = ''.join(i)
        names.append(res)

    return names


async def get_one_dapp(user_id: int, app_name: str | list):
    c.execute(
        """
        SELECT wallet_owner, wallet_treasury
        FROM apps
        WHERE user_id = ? AND app_name = ?
        """, (user_id, app_name)
    )

    return c.fetchone()


async def get_transactions_for_dapp(user_id: int, app_name: str):
    c.execute(
        """
        SELECT transaction_amount, timestamp
        FROM transactions
        WHERE user_id = ? AND app_name = ?
        """, (user_id, app_name)
    )

    return c.fetchall()


async def get_transactions_sum(user_id: int):
    """ Get transaction sum and calculate amount value in USD. """
    # Get transactions rows
    rows = await get_all_dapps(user_id)
    items = []
    # Get dapps info and store as a list of dicts
    for app_name, owner, treasury in rows:
        
        # balance = sum(transactions)
        items.append({
            "name": app_name,
            "owner": owner,
            "treasury": treasury,
        })
    # Get transactions info, sum it and append to items
    trans_rows = [
        await get_transactions_for_dapp(user_id, it["name"]) for it in items
    ]
    # Get current sol price
    symbol = "SOL"
    quotes = await get_quotes([symbol])
    result = quotes.get(symbol.upper())
    # Calculate transactions sum
    for i, trans in enumerate(trans_rows):
        balance = sum(t[0] for t in trans) if trans else 0.0
        items[i]["balance"] = balance
        items[i]["USD"] = balance * result

    return items