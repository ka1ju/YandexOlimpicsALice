from db_working import *
import pymorphy2


def return_wallets(user_id):
    u_id = [i.id for i in from_db("users", 'Users', {"username": user_id})][0]
    wallets = ['"' + i.accounts + '" - ' + str(i.bank) + ' ' +
               pymorphy2.MorphAnalyzer().parse(i.currency)[0].make_agree_with_number(i.bank).inflect({'gent'}).word + '.'
               for i in from_db("accounts", "Accounts", {"user_id": u_id})]
    return '\n'.join(wallets)
