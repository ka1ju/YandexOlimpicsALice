from db_working import *


def return_wallets():
    wallets = from_db("accounts", "accounts", )
    return '\n'.join(wallets)
