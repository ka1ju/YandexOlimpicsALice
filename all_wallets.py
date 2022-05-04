from db_working import *
import pymorphy2
import random


def return_wallets(user_id, prev):
    u_id = [i.id for i in from_db("users", 'Users', {"username": user_id})][0]
    wallets = [
               '"' + i.accounts + '" - ' + str(i.bank) + ' ' +
               pymorphy2.MorphAnalyzer().parse(i.currency)[0].make_agree_with_number(i.bank).inflect({'gent'}).word
               + '.' for i in from_db("accounts", "Accounts", {"user_id": u_id})
               ]
    for j in range(len(wallets)):
        if "тенгов" in wallets[j]:
            wallets[j] = wallets[j].replace("тенгов", "тенге")
    if len(wallets) > 0:
        answers = ["Вот ваши кошельки", "Вот список ваших счетов", "Вот все ваши кошельки", "Вот все ваши счета"]
        if prev['session']['all_wallets'] in answers:
            answers.remove(prev['session']['all_wallets'])
        return answers[random.randint(0, len(answers) - 1)] + ":\n" + '\n'.join(wallets)
    else:
        answers = ["Пока что кошельков нет", "Извините, но я не нашел у вас ни одного кошелька",
                   "Вы пока что не создали ни один счёт", "Вы пока что не создали ни один счёт",
                   "Вы ещё не добавили ни одного счёта"]
        if prev['session']['all_wallets'] in answers:
            answers.remove(prev['session']['all_wallets'])
        return answers[random.randint(0, len(answers) - 1)]
