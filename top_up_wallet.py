from db_working import *


def Popolnyt(st, user_name):
    b = st.split('и')
    user_id1 = [i.id for i in from_db("users", "Users", {"username": user_name})]
    user_id = user_id1[0]
    bd = [i.accounts for i in from_db("accounts", "Accounts", {"user_id": user_id})]
    q = []
    for j in range(len(b)):
        y = 0
        for i in bd:
            if i in b[j]:
                y = 1
                q.append(i)
        if y == 0:
            q.append(' ')
    #----------
    c = []
    if len(b) > 1:
        for i in range(len(b)):
            c.append(' '.join(b[i]).split(' '))
    else:
        c = st.split(' ')
    a1 = ['ё', 'й', 'ц', 'у', 'к', 'е', 'н', 'г', 'ш', 'щ', 'з', 'х', 'ъ', 'ф', 'ы', 'в', 'а', 'п', 'р', 'о', 'л', 'д',
          'ж', 'э', 'я', 'ч', 'с', 'м', 'и', 'т', 'ь', 'б', 'ю', 'Ё', 'Й', 'Ц', 'У', 'К', 'Е', 'Н', 'Г', 'Ш', 'Щ', 'З',
          'Х', 'Ъ', 'Ф', 'Ы', 'В', 'А', 'П', 'Р', 'О', 'Л', 'Д', 'Ж', 'Э', 'Я', 'Ч', 'С', 'М', 'И', 'Т', 'Ь', 'Б', 'Ю']
    a = []
    for j in range(len(c)):
        for i in range(len(c[j])):
            y = 0
            for k in list(c[j][i]):
                if k in a1:
                    y = 1
                    break
            if y == 0:
                a.append(c[j][i])
            else:
                a.append(' ')
    #----------
    for j in range(len(q)):
        y = 0
        if q[j] in bd:
            y = 1
            v = from_db('accounts', 'Accounts', {'accounts': q[j]})
            change_db('accounts', 'Accounts', {'accounts': q[j], 'bank': int(v[0].bank + int(a[j]))})
            return 'Баланс кошелька', q[j], 'пополнен'
        if y == 0:
            return 'У вас нет кошелька с таким названием' #??????????
    pass
