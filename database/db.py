import sqlite3


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
        transaction_amount REAL NOT NULL
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
        SELECT transaction_amount
        FROM transactions
        WHERE user_id = ? AND app_name = ?
        """, (user_id, app_name)
    )

    return c.fetchall()