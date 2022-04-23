from db_working import *


def Popolnyt(st, un):
    bd = from_db('accounts', 'Accounts')
    b = st.split('и')
    a = []
    #проверка юзера
    for i in range(len(b)):
        a.append(' '.join(b[i]).split(' '))
    x = [el.accounts for el in bd]
    y = 0
    for j in range(len(a)):
        for i in range(len(a[j])):
            if a[j][i] in x:
                y = 1
                v = from_db('accounts', 'Accounts', {'accounts': a[j][i]})
                change_db('accounts', 'Accounts', {'accounts': a[j][i], 'bank': int(v[0].bank + int(a[j][i + 2]))})
    if y == 1:
        return 'Успешно'
    else:
        return 'У вас нет кошелька с таким именем'
    pass
