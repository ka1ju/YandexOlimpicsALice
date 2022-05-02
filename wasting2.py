from db_working import to_db, from_db, change_db
import pymorphy2
import w2n
morph = pymorphy2.MorphAnalyzer()


def wasting(s, user_name, info):
    req = s.split()
    for i in range(len(req)):
        try:
            parse_it = morph.parse(req[i])
            maybe_num = parse_it[0].normal_form
            req[i] = str(w2n.word_to_num(maybe_num))
        except Exception:
            pass
    s = ' '.join(req)
    flag = True
    list = [('развлечения', ['развлечения', 'кафе', 'ресторан', 'ресторане', 'шоппинг']),
            ('продукты', ['продукты']),
            ('налоги', ['налоги', 'жкх', 'ЖКХ', 'кредит', 'ипотека', 'ипотеку']),
            ('магазины', ['магазины', 'пятёрочка', 'пятерочке', 'одежду', 'одежда', 'канцелярию', 'канцелярия']),
            ('другое', ['другое', 'алкоголь', 'кофе', 'сиграеты', 'кварплату', 'кварплата', 'подарки', 'чипсы',
                        'вкусняшки', 'техника', 'технику', 'игру', 'игры', 'попить'])]
    list2 = ['развлечения', 'кафе', 'ресторан', 'ресторане', 'шоппинг', 'продукты', 'налоги', 'жкх', 'ЖКХ', 'магазины',
             'пятёрочка', 'одежду', 'одежда', 'канцелярию', 'канцелярия', 'пятерочке', 'другое', 'алкоголь', 'кофе',
             'сиграеты', 'кварплату', 'кварплата', 'подарки', 'ипотека', 'ипотеку', 'чипсы', 'вкусняшки', 'техника',
             'технику', 'игру', 'игры', "попить"]
    user_id1 = [i.id for i in from_db("users", "Users", {"username": user_name})]
    user_id = user_id1[0]
    n = []
    N = []
    x = []
    t = []
    names = [i.accounts for i in from_db("accounts", "Accounts", {"user_id": user_id})]
    if info == {}:
        a = s.split(' и ')
        for i in range(len(a)):
            a1 = a[i].split()
            for j in range(len(a1)):
                if ord('0') <= ord(a1[j][0]) <= ord('9') and len(x) < (i + 1):
                    x.append(a1[j])
            for j in names:
                if j in a[i] and len(N) < (1 + i):
                    N.append(j)
            for j in list2:
                if j in a[i]:
                    n.append(j)
            for j in n:
                for k in list:
                    if j in k[1] and len(t) < (i + 1):
                        t.append(k[0])
            if len(x) < (i + 1):
                x.append(None)
            if len(N) < (i + 1):
                N.append(None)
            if len(t) < (i + 1):
                t.append(None)
        s = ''
        s_error = ''
        info['длина'] = 0
        long = 0
        for o in range(min(len(N), len(x), len(t))):
            if x[o] == None or N[o] == None or t[o] == None:
                if x[o] == None and N[o] == None and t[o] == None:
                    s_error += 'Извините, не совсем Вас поняла'
                elif x[o] != None and N[o] == None and t[o] == None:
                    s_error += 'Повторите пожалуйста, с какого счёта и за что списать ' + str(x[o]) + ' рублей'
                elif x[o] == None and N[o] != None and t[o] == None:
                    s_error += 'Извините, не расслышала за что и сколько вы потратили со счёта ' + N[o]
                elif x[o] == None and N[o] == None and t[o] != None:
                    s_error += 'Прошу прощения, сколько и с какого счёта вы потратили на ' + t[o]
                elif x[o] != None and N[o] != None and t[o] == None:
                    s_error += 'Извините, за что вы заплатили ' + x[o] + ' рублей из кошелька ' + N[o]
                elif x[o] != None and N[o] == None and t[o] != None:
                    s_error += 'Повторите, пожалуйста, с какого счёта списать ' + x[o] + ' рублей за ' + t[o]
                elif x[o] == None and N[o] != None and t[o] != None:
                    s_error += 'Прошу прощения, сколько вы потратили со счёта ' + N[o] + ' на ' + t[o]
                info[str(long)] = [x[o], N[o], t[o]]
                long += 1
                info['длина'] = long
            else:
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
                st = 'Успешно списано ' + str(x[o]) + ' рублей с кошелька ' + str(N[o]) + ' за ' + t[o]
                s += st
            s += s_error
    else:
        a = s.split(' и ')
        for i in range(min(len(a), info['длина'])):
            a1 = a[i].split()
            if info[str(i + 1)][0] is None:
                for j in range(len(a1)):
                    if ord('0') <= ord(a1[j][0]) <= ord('9') and info[str(i + 1)][0] == None:
                        info[str(i)][0] = a1[j]
            if info[str(i + 1)][1] == None:
                for j in names:
                    if j in a[i] and info[str(i + 1)][1] == None:
                        info[str(i + 1)][1] = j
            if info[str(i + 1)][2] == None:
                k = ''
                for j in a1:
                    if j in list2:
                        k = j
                        break
                for j in range(len(list)):
                    if k in list[i][1] and info[str(i)][2] == None:
                        info[str(i + 1)][2] = list[i][0]
        x = []
        for i in range(info['длина']):
            x.append(info[str(i + 1)][0])
            N.append(info[str(i + 1)][1])
            t.append(info[str(i + 1)][2])
        info = {}
        s = ''
        s_error = ''
        info['длина'] = 0
        long = 0
        for o in range(min(len(N), len(x), len(t))):
            if x[o] == None or N[o] == None or t[o] == None:
                if x[o] == None and N[o] == None and t[o] == None:
                    s_error += 'Извините, не совсем Вас поняла'
                elif x[o] != None and N[o] == None and t[o] == None:
                    s_error += 'Повторите пожалуйста, с какого счёта и за что списать ' + str(x[o]) + ' рублей'
                elif x[o] == None and N[o] != None and t[o] == None:
                    s_error += 'Извините, не расслышала за что и сколько вы потратили со счёта ' + N[o]
                elif x[o] == None and N[o] == None and t[o] != None:
                    s_error += 'Прошу прощения, сколько и с какого счёта вы потратили на ' + t[o]
                elif x[o] != None and N[o] != None and t[o] == None:
                    s_error += 'Извините, за что вы заплатили ' + x[o] + ' рублей из кошелька ' + N[o]
                elif x[o] != None and N[o] == None and t[o] != None:
                    s_error += 'Повторите, пожалуйста, с какого счёта списать ' + x[o] + ' рублей за ' + t[o]
                elif x[o] == None and N[o] != None and t[o] != None:
                    s_error += 'Прошу прощения, сколько вы потратили со счёта ' + N[o] + ' на ' + t[o]
                info[str(long)] = [x[o], N[o], t[o]]
                long += 1
                info['длина'] = long
            else:
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
                st = 'Успешно списано ' + str(x[o]) + ' рублей с кошелька ' + str(N[o]) + ' за ' + t[o]
                s += st
            s += s_error
    return s, info
