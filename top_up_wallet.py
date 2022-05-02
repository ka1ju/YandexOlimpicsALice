from db_working import *
import pymorphy2
morph = pymorphy2.MorphAnalyzer()


def top_up_wallet(st, user_name, k):
    if k == {}:
        b = st.split(' и ')
        user_id1 = [i.id for i in from_db("users", "Users", {"username": user_name})]
        user_id = user_id1[0]
        bd = [i.accounts for i in from_db("accounts", "Accounts", {"user_id": user_id})]
        q1 = []
        currency = ['рубль', 'рубля', 'рублей', 'евро', 'доллар', 'доллара', 'долларов', 'фунт', 'фунта', 'фунтов',
                    'йена', 'йены', 'йен', 'франк', 'франка', 'франков', 'тенге']
        cur = []
        for j in range(len(b)):
            y = 0
            for i in bd:
                if i in ''.join(b[j]):
                    y = 1
                    q1.append(i)
            if y == 0:
                q1.append(' ')
        for j in range(len(b)):
            y = 0
            for i in range(len(b[j].split(' '))):
                if b[j].split(' ')[i] in currency:
                    y = 1
                    m = morph.parse(b[j].split(' ')[i])[0].normal_form
                    cur.append(m)
            if y == 0:
                cur.append(' ')
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
        q = []
        for i in range(len(q1)):
            if q1[i] == ' ':
                li = b[i].split(' ')
                q2 = []
                for j in range(len(li)):
                    if li[j] not in words:
                        q2.append(li[j])
                q.append(' '.join(q2))
            else:
                q.append(q1[i])
        x = []
        if len(b) > 1:
            for i in range(len(b)):
                x.append(b[i].split(' '))
        else:
            x = st.split(' ')
        c = []
        for i in range(len(x)):
            if len(b) > 1:
                c1 = []
                for j in range(len(x[i])):
                    m = morph.parse(x[i][j])[0].normal_form
                    c1.append(m)
                c.append(c1)
            else:
                m = morph.parse(x[i])[0].normal_form
                c.append(m)
        s = []
        if len(c) > 1:
            for i in range(len(c)):
                s1 = []
                for j in range(len(c[i])):
                    if c[i][j] in millions:
                        s1.append('1000000')
                    elif c[i][j] in thousands:
                        s1.append('1000')
                    elif c[i][j] in units:
                        s1.append(units[c[i][j]])
                    elif c[i][j] in dozens:
                        s1.append(dozens[c[i][j]])
                    elif c[i][j] in hundreds:
                        s1.append(hundreds[c[i][j]])
                    s1.append(0)
                s.append(s1)
        else:
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
        summa = []
        if len(s) > 1:
            for i in range(len(s)):
                y = 0
                for j in range(len(s[i]) - 1):
                    if s[i][j + 1] == '1000' or s[i][j + 1] == '1000000':
                        if s[i][j] != '1000' and s[i][j] != '1000000':
                            y += int(s[i][j])
                            y = y * int(s[i][j + 1])
                    else:
                        if s[i][j] != '1000' and s[i][j] != '1000000':
                            y += int(s[i][j])
                summa.append(y)
                y = 0
        else:
            y = 0
            for i in range(len(s) - 1):
                if s[i + 1] == '1000' or s[i + 1] == '1000000':
                    if s[i] != '1000' and s[i] != '1000000':
                        y += int(s[i])
                        y = y * int(s[i + 1])
                else:
                    if s[i] != '1000' and s[i] != '1000000':
                        y += int(s[i])
                summa.append(y)
                y = 0
        for i in range(len(q)):
            if q[i] == None:
                ret = 'Какой кошелёк вы хотите пополнить на ' + summa[i] + '?', {'username': q}
                return ret
            elif summa[i] == None:
                ret = 'На какую сумму вы хотите пополнить кошелёк ' + q[i] + '?', {'summa': summa}
                return ret
        ret = ''
        for j in range(len(q)):
            if q[j] in bd:
                currencyN = from_db("accounts", "Accounts", {"user_id": user_id, "accounts": q[j]})[0]
                if cur[j] != currencyN.currency and cur[j] != ' ':
                    ret += 'Извините, валюта не соответствует валюте кошелька: ' + q[j] + '\n'
                    continue
                v = [i.bank for i in from_db('accounts', 'Accounts', {'accounts': q[j], 'user_id': user_id})]
                v1 = v[0]
                change_db('accounts', 'Accounts', {'bank': int(v1) + summa[j]}, {'accounts': q[j], 'user_id': user_id})
                ret += 'Баланс кошелька "' + q[j] + '" пополнен' + '\n'
            elif q[j] not in words:
                ret += 'У вас нет кошелька с названием: ' + q[j] + '\n'
        return ret, {}
    else:
        b = st.split(' и ')
        user_id1 = [i.id for i in from_db("users", "Users", {"username": user_name})]
        user_id = user_id1[0]
        bd = [i.accounts for i in from_db("accounts", "Accounts", {"user_id": user_id})]
        q1 = []
        currency = ['рубль', 'рубля', 'рублей', 'евро', 'доллар', 'доллара', 'долларов', 'фунт', 'фунта', 'фунтов', 'йена',
                    'йены', 'йен', 'франк', 'франка', 'франков', 'тенге']
        cur = []
        for j in range(len(b)):
            y = 0
            for i in bd:
                if i in ''.join(b[j]):
                    y = 1
                    q1.append(i)
            if y == 0:
                q1.append(' ')
        for j in range(len(b)):
            y = 0
            for i in range(len(b[j].split(' '))):
                if b[j].split(' ')[i] in currency:
                    y = 1
                    m = morph.parse(b[j].split(' ')[i])[0].normal_form
                    cur.append(m)
            if y == 0:
                cur.append(' ')
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
        # -----------------------------
        q = []
        for i in range(len(q1)):
            if q1[i] == ' ':
                li = b[i].split(' ')
                q2 = []
                for j in range(len(li)):
                    if li[j] not in words:
                        q2.append(li[j])
                q.append(' '.join(q2))
            else:
                q.append(q1[i])
        x = []
        if len(b) > 1:
            for i in range(len(b)):
                x.append(b[i].split(' '))
        else:
            x = st.split(' ')
        c = []
        for i in range(len(x)):
            if len(b) > 1:
                c1 = []
                for j in range(len(x[i])):
                    m = morph.parse(x[i][j])[0].normal_form
                    c1.append(m)
                c.append(c1)
            else:
                m = morph.parse(x[i])[0].normal_form
                c.append(m)
        s = []
        if len(c) > 1:
            for i in range(len(c)):
                s1 = []
                for j in range(len(c[i])):
                    if c[i][j] in millions:
                        s1.append('1000000')
                    elif c[i][j] in thousands:
                        s1.append('1000')
                    elif c[i][j] in units:
                        s1.append(units[c[i][j]])
                    elif c[i][j] in dozens:
                        s1.append(dozens[c[i][j]])
                    elif c[i][j] in hundreds:
                        s1.append(hundreds[c[i][j]])
                    s1.append(0)
                s.append(s1)
        else:
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
        summa = []
        if len(s) > 1:
            for i in range(len(s)):
                y = 0
                for j in range(len(s[i]) - 1):
                    if s[i][j + 1] == '1000' or s[i][j + 1] == '1000000':
                        if s[i][j] != '1000' and s[i][j] != '1000000':
                            y += int(s[i][j])
                            y = y * int(s[i][j + 1])
                    else:
                        if s[i][j] != '1000' and s[i][j] != '1000000':
                            y += int(s[i][j])
                summa.append(y)
                y = 0
        else:
            y = 0
            for i in range(len(s) - 1):
                if s[i + 1] == '1000' or s[i + 1] == '1000000':
                    if s[i] != '1000' and s[i] != '1000000':
                        y += int(s[i])
                        y = y * int(s[i + 1])
                else:
                    if s[i] != '1000' and s[i] != '1000000':
                        y += int(s[i])
                summa.append(y)
                y = 0
        username = k['username']
        summaO = k['summa']
        for i in range(len(username)):
            if username[i] == None:
                username[i] = q[0]
                q.pop(0)
            elif summaO[i] == None:
                summaO[i] = summa[0]
                summa.pop(0)
        q.clear()
        summa.clear()
        q = username.copy()
        summa = summaO.copy()
        #---------------------
        ret = ''
        for j in range(len(q)):
            if q[j] in bd:
                currencyN = from_db("accounts", "Accounts", {"user_id": user_id, "accounts": q[j]})[0]
                if cur[j] != currencyN.currency and cur[j] != ' ':
                    ret += 'Извините, валюта не соответствует валюте кошелька: ' + q[j] + '\n'
                    continue
                v = [i.bank for i in from_db('accounts', 'Accounts', {'accounts': q[j], 'user_id': user_id})]
                v1 = v[0]
                change_db('accounts', 'Accounts', {'bank': int(v1) + summa[j]}, {'accounts': q[j], 'user_id': user_id})
                ret += 'Баланс кошелька "' + q[j] + '" пополнен' + '\n'
            elif q[j] not in words:
                ret += 'У вас нет кошелька с названием: ' + q[j] + '\n'
        return ret, {}
