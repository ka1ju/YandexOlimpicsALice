from db_working import *
import datetime
import random


def authorization(user_name, inp):
    a = from_db('users', 'Users', {'username': user_name})
    if a:
        variants = ['чем могу помочь?', 'что вам угодно?', 'чем займемся сейчас?']
        return 'Приветствую, рад снова видеть, ' + random.choice(variants)
    else:
        to_db('users', 'Users', ('username', 'password'), (user_name, '1'))
        print(user_name)
        return f'Привет, меня зовут Олег. Я создан для того чтобы вести учёт ваших трат. ' \
               f'Вот краткий список моих функций:\n' +  "\n".join([str(i) for i in inp])


def statistic(string, usr_name, k):
    if string[-1] == '.':
        string = string[:-1]
    if k == {}:
        a = from_db('users', 'Users', {'username': usr_name})[0]
        account_element_id = a.id
        yuy = from_db('accounts', 'Accounts', {'user_id': account_element_id})
        names = [i.accounts for i in yuy]
        ac = ''
        m = datetime.datetime.now().month
        y = datetime.datetime.now().year
        for i in names:
            if i in string:
                ac = i
                break
        if ac != '':
            yuy = from_db('accounts', 'Accounts', {'user_id': account_element_id, 'accounts': ac})[0]
            d = {'развлечения': 0, 'продукты': 0, 'налоги': 0, 'магазины': 0, 'другое': 0, "пополнения": 0}
            spend_all = 0
            ok = from_db('waste', 'Waste', {'account_id': yuy.id})
            for i in ok:
                k = 0
                dad = i.date.split('.')
                if 'за все время' in string:
                    k = 1
                if 'год' in string:
                    if int(dad[2]) == y:
                        k = 1
                if int(dad[1]) == m and int(dad[2]) == y:
                    k = 1
                if k == 1:
                    d[i.category] += i.count
                    spend_all += i.count
            return f'В общем было потрачено: {spend_all}\nНа развлечения: {d["развлечения"]}\n' \
                   f'На продукты: {d["продукты"]}\n' \
                   f'На оплату налогов: {d["налоги"]}\n' \
                   f'В магазинах: {d["магазины"]}\n' \
                   f'На другое: {d["другое"]}\n' \
                   f'Пополнения : {d["пополнения"]}', {}
        else:
            return 'Уточните, пожалуйста, с какого счета нужно вывести статистику.', {'flag': 'koshel'}
    else:
        a = from_db('users', 'Users', {'username': usr_name})[0]
        account_element_id = a.id
        yuy = from_db('accounts', 'Accounts', {'user_id': account_element_id})
        names = [i.accounts for i in yuy]
        ac = ''
        m = datetime.datetime.now().month
        y = datetime.datetime.now().year
        for i in names:
            if i in string:
                ac = i
                break
        if ac != '':
            yuy = from_db('accounts', 'Accounts', {'user_id': account_element_id, 'accounts': ac})[0]
            d = {'развлечения': 0, 'продукты': 0, 'налоги': 0, 'магазины': 0, 'другое': 0}
            spend_all = 0
            ok = from_db('waste', 'Waste', {'account_id': yuy.id})
            for i in ok:
                k = 0
                dad = i.date.split('.')
                if 'за все время' in string:
                    k = 1
                if 'год' in string:
                    if int(dad[2]) == y:
                        k = 1
                if int(dad[1]) == m and int(dad[2]) == y:
                    k = 1
                if k == 1:
                    d[i.category] += i.count
                    spend_all += i.count
            return f'В общем было потрачено: {spend_all}\nНа развлечения: {d["развлечения"]}\n' \
                   f'На продукты: {d["продукты"]}\n' \
                   f'На оплату налогов: {d["налоги"]}\n' \
                   f'В магазинах: {d["магазины"]}\n' \
                   f'На другое: {d["другое"]}', {}
        else:
            return 'Простите, я вас не понял, отмена операции', {}