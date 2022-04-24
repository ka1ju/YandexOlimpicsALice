from db_working import *


def return_wallets(user_id):
    wallets = [i for i in from_db("accounts", "Accounts", {"user_id": user_id})]
    return wallets
