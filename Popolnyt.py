from db_working import *


def Popolnyt(st, un):
    bd = from_db('accounts', 'Accounts')
    b = st.split('и')
    a = []
    #проверка юзера
    for i in range(len(b)):
        a.append(' '.join(b[i]).split(' '))
    for j in range(len(a)):
        for i in range(len(a[j])):
            if a[j][i] in [el.accounts for el in bd]:
                v = from_db('accounts', 'Accounts', {'accounts': a[j][i]})
                change_db('accounts', 'Accounts', {'accounts': a[j][i], 'bank': int(v[0].bank + int(a[j][i + 2]))})
    return 'успешно'
    pass
