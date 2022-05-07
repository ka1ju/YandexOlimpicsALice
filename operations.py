from db_working import *
import datetime
import pymorphy2


def operations(userName, userMessage):
    userId = [i.id for i in from_db("users", "Users", {"username": userName})][0]
    result = ["Ваши траты за последний месяц:"]
    currencies = {}
    walletsId = [i.id for i in from_db("accounts", "Accounts", {"user_id": userId})]
    for i in from_db("waste", "Waste"):
        walletId = i.account_id
        if walletId in walletsId:
            if i.category != "":
                currency = [i.currency for i in from_db("accounts", "Accounts", {"id": walletId})][0]
                if currency in currencies:
                    currencies[currency] += int(i.count)
                else:
                    currencies[currency] = int(i.count)
    for i in currencies:
        if i == "тенге":
            result.append(str(currencies[i]) + " " + i)
        else:
            cur = pymorphy2.MorphAnalyzer().parse(i)[0].make_agree_with_number(currencies[i]).inflect({'gent'}).word
            result.append(str(currencies[i]) + " " + cur)
    return "\n".join(result)


print(operations("AQAAAAAjstOuAAfaP9kRfOsQJ00rlrOmg7BlREQ", "nigger"))
