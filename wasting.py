from db_working import to_db, from_db, change_db, remove_from_db


def wasting(s, user_name):
    flag = True
    list = [('развлечения', ['развлечения', 'кафе', 'ресторан', 'ресторане', 'шоппинг', '']),
            ('продукты', ['продукты']),
            ('налоги', ['налоги', 'жкх', 'ЖКХ']),
            ('магазины', ['магазины', 'пятёрочка', 'пятерочке', 'одежду', 'одежда', 'канцелярию', 'канцелярия']),
            ('другое', ['другое', 'алкоголь', 'кофе', 'сиграеты', 'кварплату', 'кварплата', 'подарки'])]
    list2 = ['развлечения', 'кафе', 'ресторан', 'ресторане', 'шоппинг', 'продукты', 'налоги', 'жкх', 'ЖКХ', 'магазины',
             'пятёрочка', 'одежду', 'одежда', 'канцелярию', 'канцелярия', 'пятерочке', 'другое', 'алкоголь', 'кофе',
             'сиграеты', 'кварплату', 'кварплата', 'подарки']
    user_id1 = [i.id for i in from_db("users", "Users", {"username": user_name})]
    user_id = user_id1[0]
    n = ''
    N = ''
    x = 0
    t = ''
    a = s.split()
    for i in range(0, len(a)):
        if ord('0') <= ord(a[i][0]) <= ord('9'):
            x = int(a[i])
    names = [i.accounts for i in from_db("accounts", "Accounts", {"user_id": user_id})]
    for i in names:
        if i in s:
            N = i
            break
    for i in a:
        if i in list2:
            n = i
            break
    for i in range(len(list)):
        if n in list[i][1]:
            t = list[i][0]
    if x == 0 or N == '' or t == '':
        flag = False
    if flag:
        id1 = [i.id for i in from_db("accounts", "Accounts", {"accounts": N, "user_id": user_id})]
        id = id1[0]
        summ1 = [j.bank for j in from_db("accounts", "Accounts", {"accounts": N, "user_id": user_id})]
        summ = summ1[0]
        summ -= x
        change_db("accounts", "Accounts", {"bank": summ}, {"accounts": N, "user_id": user_id})
        newcount1 = [k.count for k in from_db("waste", "Waste", {"account_id": id, "category": t})]
        if len(newcount1) != 0:
            newcount = newcount1[0]
            newcount += x
            change_db("waste", "Waste", {"count": newcount}, {"account_id": id, "category": t})
        else:
            to_db("waste", "Waste", ("account_id", "category", "count"), (id, t, x))
        st = 'Успешно списано ' + str(x) + ' рублей с кошелька ' + N + ' за ' + t
        return st
    else:
        return 'Извините, не совсем Вас поняла'
# частично сделал распознавание
