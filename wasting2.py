from db_working import *


def wasting(s, user_name):
    flag = True
    list = [('развлечения', ['развлечения', 'кафе', 'ресторан', 'ресторане', 'шоппинг']),
            ('продукты', ['продукты']),
            ('налоги', ['налоги', 'жкх', 'ЖКХ', 'кредит', 'ипотека', 'ипотеку']),
            ('магазины', ['магазины', 'пятёрочка', 'пятерочке', 'одежду', 'одежда', 'канцелярию', 'канцелярия']),
            ('другое', ['другое', 'алкоголь', 'кофе', 'сигареты', 'квартплату', 'квартплата', 'подарки', 'чипсы',
                        'вкусняшки', 'техника', 'технику', 'игру', 'игры'])]
    list2 = ['развлечения', 'кафе', 'ресторан', 'ресторане', 'шоппинг', 'продукты', 'налоги', 'жкх', 'ЖКХ', 'магазины',
             'пятёрочка', 'одежду', 'одежда', 'канцелярию', 'канцелярия', 'пятерочке', 'другое', 'алкоголь', 'кофе',
             'сигареты', 'квартплату', 'квартплата', 'подарки', 'ипотека', 'ипотеку', 'чипсы', 'вкусняшки', 'техника',
             'технику', 'игру', 'игры']
    user_id1 = [i.id for i in from_db("users", "Users", {"username": user_name})]
    user_id = user_id1[0]
    n = []
    N = []
    x = []
    t = []
    a = s.split()
    for i in range(0, len(a)):
        if ord('0') <= ord(a[i][0]) <= ord('9'):
            x.append(a[i])
    names = [i.accounts for i in from_db("accounts", "Accounts", {"user_id": user_id})]
    for i in range(len(a)):
        s = a[i]
        for j in range(i + 1, len(a)):
            s += a[j]
            if s in names:
                N.append(i)
                break
    for i in a:
        if i in list2:
            n.append(i)
    for i in range(len(list)):
        for j in n:
            if j in list[i][1]:
                t.append(j)
    s = ''
    for o in range(min(len(N), len(x), len(t))):
        if x[o] == 0 or N[o] == '' or t[o] == '':
            flag = False
        if flag:
            id1 = [i.id for i in from_db("accounts", "Accounts", {"accounts": N[o], "user_id": user_id})]
            id = id1[0]
            summ1 = [j.bank for j in from_db("accounts", "Accounts", {"accounts": N[o], "user_id": user_id})]
            summ = summ1[0]
            summ -= x[o]
            change_db("accounts", "Accounts", {"bank": summ}, {"accounts": N[o], "user_id": user_id})
            newcount1 = [k.count for k in from_db("waste", "Waste", {"account_id": id, "category": t[o]})]
            if len(newcount1) != 0:
                newcount = newcount1[0]
                newcount += x[o]
                change_db("waste", "Waste", {"count": newcount}, {"account_id": id, "category": t[o]})
            else:
                to_db("waste", "Waste", ("account_id", "category", "count"), (id, t, x))
            st = 'Успешно списано ' + str(x[o]) + ' рублей с кошелька ' + N[o] + ' за ' + t[o]
            s += st
            s += '\n'
        else:
            s += 'Извините, не совсем Вас поняла'
            s += '\n'
    return s
# частично сделал распознавание
