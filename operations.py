from db_working import *
import datetime
from datetime import timedelta
import pymorphy2


def operations(userName, userMessage, state):
    if state == {}:
        if "месяц" in userMessage:
            date = datetime.date.today() - timedelta(days=30)
            operationsList = ["Ваши операции за последний месяц:"]
        elif "год" in userMessage:
            date = datetime.date.today() - timedelta(days=365)
            operationsList = ["Ваши операции за последний год:"]
        else:
            date = datetime.date.today() - timedelta(weeks=1)
            operationsList = ["Ваши операции за последнюю неделю:"]
        userId = [i.id for i in from_db("users", "Users", {"username": userName})][0]
        walletId = ""
        for i in from_db("accounts", "Accounts", {"user_id": userId}):
            if i.accounts in userMessage:
                walletId = i.id
                break
        if type(walletId) == str:
            return "По какому кошельку вы хотите вывести операции", \
                   {"date": {"day": date.day, "month": date.month, "year": date.year}, "operationsList": operationsList}
        currency = [i.currency for i in from_db("accounts", "Accounts", {"id": walletId})][0]
        for i in from_db("waste", "Waste"):
            d = i.date.split(".")
            if datetime.date(year=int(d[2]), month=int(d[1]), day=int(d[0])) > date:
                if i.account_id == walletId:
                    if currency != "тенге":
                        cur = pymorphy2.MorphAnalyzer().parse(currency)[0].make_agree_with_number(i.count).inflect(
                            {'gent'}).word
                    else:
                        cur = currency
                    if i.category == "пополнение":
                        operationsList.append(f"Получено {i.count} {cur}")
                    else:
                        operationsList.append(f"Потрачено {i.count} {cur} на {i.category}")
        return "\n".join(operationsList), {}
    elif "date" in state:
        date = datetime.date(year=state['date']['year'], month=state['date']['month'], day=state["date"]['day'])
        operationsList = state["operationsList"]
        userId = [i.id for i in from_db("users", "Users", {"username": userName})][0]
        walletId = ""
        for i in from_db("accounts", "Accounts", {"user_id": userId}):
            if i.accounts in userMessage:
                walletId = i.id
                break
        if type(walletId) == str:
            return "Такого кошелька не существует, повторите название", \
                   {"date": {"day": date.day, "month": date.month, "year": date.year}, "operationsList": operationsList}
        currency = [i.currency for i in from_db("accounts", "Accounts", {"id": walletId})][0]
        for i in from_db("waste", "Waste"):
            d = i.date.split(".")
            if datetime.date(year=int(d[2]), month=int(d[1]), day=int(d[0])) > date:
                if i.account_id == walletId:
                    if currency != "тенге":
                        cur = pymorphy2.MorphAnalyzer().parse(currency)[0].make_agree_with_number(i.count).inflect(
                            {'gent'}).word
                    else:
                        cur = currency
                    if i.category == "пополнение":
                        operationsList.append(f"Получено {i.count} {cur}")
                    else:
                        operationsList.append(f"Потрачено {i.count} {cur} на {i.category}")
        return "\n".join(operationsList), {}
    return "Что-то пошло нахуй, например твоя мать", {}


# print(operations("AQAAAAAjstOuAAfaP9kRfOsQJ00rlrOmg7BlREQ", "негр", {'date': datetime.date(2021, 5, 8), 'operationsList': ['Ваши операции за последний год:']}))
