from db_working import to_db, remove_from_db, from_db


def create_wallet(req):
    req = req.lower().split()
    req_lst = ["создай", "счёт", "счета", "кошелёк", "кошельки", "с", "на", "названием", "название", "названиями", "который", "которые", "назваются", "назвается", "суммой", "начальной", "номинал", "номиналом", "в", "привет", "пожалуйста", "пока", "спасибо", "а", "ещё"]
    cur_lst = ["рубль", "рубля", "рублей", "евро", "доллар", "долларов", "доллара", "тенге"]
    cur_d = {
                "рубль": "рубль", "рубля": "рубль", "рублей": "рубль",
                "евро": "евро",
                "доллар": "доллар", "долларов": "доллар", "доллара": "доллар",
                "тенге": "тенге"}
    lst = []
    c = False
    wait = False
    for it in req:
        if it.strip(",") not in req_lst and it.strip(",").isalpha() and it.strip(",") not in cur_lst:
            lst.append(it.strip(","))
            c = True
            wait = True
        if "," in it and c:
            lst.append("и")
            c = False
        if wait and it.strip(",").isdigit():
            wait = False
            lst.append(it)
        if it.strip(",") in cur_lst:
            lst.append(it.strip(","))
    lst = " ".join(lst).split(" и ")
    res_d = {}
    for el in lst:
        el = el.split()
        k, b_k, c_k = "", 0, "рубль"
        for item in el:
            if item.isalpha() and item not in cur_lst:
                k += item + " "
            elif item.isdigit():
                b_k = int(item)
            elif item in cur_lst:
                c_k = cur_d[item]
        res_d[k.strip()] = (b_k, c_k)
    for i in res_d:
        to_db("accounts", "Accounts", ("accounts", "bank", "currency"), (i, res_d[i][0], res_d[i][-1]))
    res_lst = []
    import pymorphy2
    morph = pymorphy2.MorphAnalyzer()
    for k in res_d:
        t = morph.parse(res_d[k][1])[0]
        res_lst.append(f'"{k.capitalize()}" с суммой {res_d[k][0]} {t.make_agree_with_number(res_d[k][0]).word}\n')
    if len(res_d.keys()) > 1:
        print(f"Созданы счета:\n{''.join(res_lst)}")
    else:
        print(f"Создан счёт {''.join(res_lst)}")


def delete_wallet(req):
    req = req.lower().split()
    req_lst = ["удали", "счёт", "счета", "кошелёк", "кошельки", "с", "на", "названием", "название", "названиями", "который", "которые", "назваются", "назвается", "привет", "пожалуйста", "пока", "спасибо", "а", "ещё"]
    lst = []
    for it in req:
        if it not in req_lst:
            lst.append(it.strip(","))
    lst = " ".join(lst).split(" и ")
    no = []
    yes = []
    import pymorphy2
    morph = pymorphy2.MorphAnalyzer()
    for i in lst:
        if len(from_db("accounts", "Accounts", {"accounts": i})) == 0:
            no.append(i)
        else:
            remove_from_db("accounts", "Accounts", {"accounts": i})
            yes.append(i)
    if len(no) > 0:
        if len(no) > 1:
            print(f"""Счетов "{'", "'.join(no)}" не существет""")
        else:
            print(f'Счёта "{no[0]}" не существует')
    if len(yes) > 0:
        if len(yes) > 1:
            print(f"""Счета "{'", "'.join(yes)}" были удалены""")
        else:
            print(f'Счёт "{yes[0]}" был удалён')


# create_wallet("создай счёт как дела 500 рублей")
# create_wallet("привет! создай счёт база на 500 долларов и счёт негры, а ещё как какать 500")
# delete_wallet("удали счёт база и негры")

# проверка на пользователя