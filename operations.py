from db_working import *
import datetime
from datetime import timedelta
import pymorphy2


def operations(userName, userMessage):
    userId = [i.id for i in from_db("users", "Users", {"username": userName})][0]
    walletId = ""
    for i in from_db("accounts", "Accounts", {"user_id": userId}):
        if i.accounts in userMessage:
            walletId = i.id
            break
    if type(walletId) == str:
        return "Извините, такого кошелька не существует"
    if "месяц" in userMessage:
        date = datetime.date.today() - timedelta(days=30)
        result = ["Ваши операции за последний месяц:"]
    elif "год" in userMessage:
        date = datetime.date.today() - timedelta(days=365)
        result = ["Ваши операции за последний год:"]
    else:
        date = datetime.date.today() - timedelta(weeks=1)
        result = ["Ваши операции за последнюю неделю:"]
    operationsList = ["Вот ваши операции:"]
    currency = [i.currency for i in from_db("accounts", "Accounts", {"id": walletId})][0]
    for i in from_db("waste", "Waste"):
        d = i.date.split(".")
        if datetime.date(year=int(d[2]), month=int(d[1]), day=int(d[0])) > date:
            if i.account_id == walletId:
                if currency != "тенге":
                    cur = pymorphy2.MorphAnalyzer().parse(currency)[0].make_agree_with_number(i.count).inflect({'gent'}).word
                else:
                    cur = currency
                if i.category == "":
                    operationsList.append(f"Получено {i.count} {cur}")
                else:
                    operationsList.append(f"Потрачено {i.count} {cur} на {i.category}")
    return "\n".join(operationsList)


# print(operations("AQAAAAAjstOuAAfaP9kRfOsQJ00rlrOmg7BlREQ", "Выведи все мои операции по счёту тест"))
