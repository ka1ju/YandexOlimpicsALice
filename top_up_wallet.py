from db_working import *
import pymorphy2
morph = pymorphy2.MorphAnalyzer()


def top_up_wallet(st, user_name):
    b = st.split(' и ')
    user_id1 = [i.id for i in from_db("users", "Users", {"username": user_name})]
    user_id = user_id1[0]
    bd = [i.accounts for i in from_db("accounts", "Accounts", {"user_id": user_id})]
    q = []
    for j in range(len(b)):
        y = 0
        for i in bd:
            if i in ''.join(b):
                y = 1
                q.append(i)
        if y == 0:
            q.append(' ')
    # ----------
    c = []
    x = []
    if len(b) > 1:
        for i in range(len(b)):
            x.append(' '.join(b[i]).split(' '))
    else:
        x = st.split(' ')
    words = ["кошел", "счёт", "счета", "кошелёк", "кошельки", "с", "на", "названием", "название", "названиями",
             "который", "которые", "назваются", "назвается", "привет", "пожалуйста", "пока", "спасибо", "а", "ещё",
             'пополни']

    units = {'один': '1', 'два': '2', 'три': '3', 'четыре': '4', 'пять': '5', 'шесть': '6', 'семь': '7',
             'восемь': '8', 'девять': '9', 'десять': '10', 'одиннадцать': '11', 'двенадцать': '12',
             'тринадцать': '13', 'четырнадцать': '14', 'пятнадцать': '15', 'шестнадцать': '16', 'семнадцать': '17',
             'восемнадцать': '18', 'девятнадцать': '19'}
    dozens = {'двадцать': '20', 'тридцать': '30', 'сорок': '40', 'пятьдесят': '50', 'шестьдесят': '60',
              'семьдесят': '70', 'восемьдесят': '80', 'девяносто': '90'}
    hundreds = {'сто': '100', 'двести': '200', 'триста': '300', 'четыреста': '400',  'пятьсот': '500',
                'шестьсот': '600', 'семьсот': '700', 'восемьсот': '800', 'девятьсот': '900'}
    thousands = ['тысяча', 'тысячи', 'тысяч']
    millions = ['миллион', 'миллиона', 'миллионов']
    c = []
    for i in range(len(x)):
        m = morph.parse(x[i])[0].normal_form
        c.append(m)
    s = []
    for i in range(len(c)):
        if c[i] in millions:
            s.append('1000000')
        elif c[i] in thousands:
            s.append('1000')
        elif c[i] in units:
            s.append(units[c[i]])
        elif c[i] in dozens:
            s.append(dozens[c[i]])
        elif c[i] in hundreds:
            s.append(hundreds[c[i]])
    s.append(0)
    summa = 0
    y = 0
    for i in range(len(s) - 1):
        if s[i + 1] == '1000' or s[i + 1] == '1000000':
            if s[i] != '1000' and s[i] != '1000000':
                y += int(s[i])
                y = y * int(s[i + 1])
        else:
            if s[i] != '1000' and s[i] != '1000000':
                y += int(s[i])
        summa += y
        y = 0
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
    # ----------
    for j in range(len(q)):
        if q[j] in bd:
            v = [i.bank for i in from_db('accounts', 'Accounts', {'accounts': q[j], 'user_id': user_id})]
            v1 = v[0]
            change_db('accounts', 'Accounts', {'bank': int(v1) + summa}, {'accounts': q[j], 'user_id': user_id})
            print(int(v1 + summa))
            ret = 'Баланс кошелька "' + q[j] + '" пополнен'
            return ret
        elif q[j] not in words:
            return 'У вас нет кошелька с названием:', q[j]
            v = from_db('accounts', 'Accounts', {'accounts': q[j]})
            change_db('accounts', 'Accounts', {'accounts': q[j], 'bank': int(v[0].bank + int(a[j]))})
            return 'Баланс кошелька', q[j], 'пополнен'
        if y == 0:
            return 'У вас нет кошелька с таким названием'  # ??????????
    pass

