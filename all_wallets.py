from db_working import *
import pymorphy2
import random
import os
import logging


def return_wallets(user_id):
    u_id = [i.id for i in from_db("users", 'Users', {"username": user_id})][0]
    wallets = ['"' + i.accounts + '" - ' + str(i.bank) + ' ' +
               pymorphy2.MorphAnalyzer().parse(i.currency)[0].make_agree_with_number(i.bank).inflect({'gent'}).word
               + '.' for i in from_db("accounts", "Accounts", {"user_id": u_id})]
    if len(wallets) > 0:
        return "Вот ваши кошельки:\n" + '\n'.join(wallets)
    else:
        answers = ["Пока что кошельков нет", "Извините, но я не нашел у вас ни одного кошелька.",
                   "Вы пока что не создали ни один счёт"]
        message = open("prev_alice_message.txt", "r", encoding="utf-8")
        m = message.read()
        if m in answers:
            answers.remove(m)
        message.close()
        index = random.randint(0, len(answers) - 1)
        answer = answers[index]
        os.remove("prev_alice_message.txt")
        with open("prev_alice_message.txt", "w", encoding="utf-8") as out:
            out.write(answer)
        return answer
