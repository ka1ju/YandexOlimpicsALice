from db_working import *


def authorization(usr_name):
    a = from_db('users', 'Users', {'username' :usr_name})
    if a:
        return 'Приветствую, приятного пользования'
    else:
        to_db('users', 'Users', ['username', 'password'], [usr_name, '1'])
        return 'Привет, меня зовут Олег. Я создан для того чтобы вести учёт ваших трат. Вот краткий список моих функций:\
                Добавление кошелька\
                Удаление кошелька\
                Зачисление денег на счёт\
                Снятие или трата денег со счёта\
                Вывод статистики\
                Вывод информации о счёте'


def statistic(str, usr_name):
    a = from_db('users', 'Users', {'username': usr_name})[0]
    id = a.id
    yuy = from_db('accounts', 'Accounts', {'user_id' :id})
    names = [i.accounts for i in yuy]
    ac = ''
    for i in names:
        if i in str.split():
            ac = i
    if ac != '':
        yuy = from_db('accounts', 'Accounts', {'user_id': id, 'accounts' :ac})[0]
        d = {'развлечения': 0, 'продукты':0, 'налоги':0, 'магазины':0, 'другое':0}
        all = 0
        ok = from_db('waste', 'Waste', {'account_id' :yuy.id})
        for i in ok:
            d[i.category] += i.count
            all += i.count
        return f'В общем было потрачено: {all}\nНа развлечения: {d["развлечения"]}\n' \
               f'На продукты: {d["продукты"]}\n' \
               f'На оплату налогов: {d["налоги"]}\n' \
               f'В магазинах: {d["магазины"]}' \
               f'На другое: {d["другое"]}'
    else:
        return 'Уточните, пожалуйста, с какого счета нужно вывести статистику.'


#C:\Users\talek\Desktop\ngrok