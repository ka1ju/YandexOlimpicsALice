# -*- coding: utf-8 -*-
from skills.YandexOlympicsAlice.db_working import to_db, remove_from_db, from_db
from skills.YandexOlympicsAlice import w2n
import pymorphy2
import random

morph = pymorphy2.MorphAnalyzer()


def create_wallet(req, user_ya_id, k=None):
    if k is None:
        k = {}
    req_lst = ["олег", "создай", "открой", "открыть", "создать", "добавь", "новый", "добавить", "можно", "можешь", "счет",
               "счёт", "счета", "кошелек", "кошелёк", "кошельки", "с", "названием", "название",
               "названиями", "который", "которые", "называются", "называется", "суммой", "начальной",
               "номинал", "номиналом", "в", "привет", "пожалуйста", "пока", "спасибо", "а", "ещё", "еще"]
    if len(k) == 0:
        user_id = [i.id for i in from_db("users", "Users", {"username": user_ya_id})][0]
        req = req.lower().split()
        cur_lst = ['доллар', 'доллара', 'доллару', 'доллар', 'долларом', 'долларе', 'доллары', 'долларов', 'долларам',
                   'доллары', 'долларами', 'долларах', 'рубль', 'рубля', 'рублю', 'рубль', 'рублём', 'рубле',
                   'рубли', 'рублей', 'рублям', 'рубли', 'рублями', 'рублях', 'юань', 'юаня', 'юаню', 'юань',
                   'юанем', 'юане', 'юани', 'юаней', 'юаням', 'юани', 'юанями', 'юанях', 'евро', 'тенге']
        cur_d = {'доллар': 'доллар', 'доллара': 'доллар', 'доллару': 'доллар', 'долларом': 'доллар',
                 'долларе': 'доллар',
                 'доллары': 'доллар', 'долларов': 'доллар', 'долларам': 'доллар', 'долларами': 'доллар',
                 'долларах': 'доллар',
                 'рубль': 'рубль', 'рубля': 'рубль', 'рублю': 'рубль', 'рублём': 'рубль', 'рубле': 'рубль',
                 'рубли': 'рубль',
                 'рублей': 'рубль', 'рублям': 'рубль', 'рублями': 'рубль', 'рублях': 'рубль', 'юань': 'юань',
                 'юаня': 'юань',
                 'юаню': 'юань', 'юанем': 'юань', 'юане': 'юань', 'юани': 'юань', 'юаней': 'юань', 'юаням': 'юань',
                 'юанями': 'юань', 'юанях': 'юань', 'евро': 'евро', 'тенге': 'тенге'}
        for i in range(len(req)):
            try:
                parse_it = morph.parse(req[i])
                maybe_num = parse_it[0].normal_form
                req[i] = str(w2n.word_to_num(maybe_num))
            except Exception:
                pass
        lst = []
        c = False
        wait = False
        for it in req:
            it = it.strip(".")
            it = it.strip("-")
            if it.strip(",") not in req_lst and it.strip(",").isalpha() and it.strip(",") not in cur_lst:
                lst.append(it.strip(","))
                c = True
                wait = True
            if "," in it and c:
                lst.append("и")
                c = False
            if wait and it.isdigit():
                wait = False
                lst.append(it)
            if it.strip(",") in cur_lst:
                if len(lst) == 0 or (True not in [x.isdigit() for x in lst]):
                    lst.append("0")
                lst.append(it.strip(","))
        for i in range(len(lst)):
            try:
                if lst[i] == "на" and (lst[i + 1].isdigit() or lst[i + 1] in ["сумму", "сумма"]):
                    lst[i] = ""
            except Exception:
                pass
        lst.append("")
        lst = " ".join(lst).split(" и ")
        if lst[-1] == "":
            lst.remove(lst[-1])
        for i in range(len(lst)):
            lst[i] = lst[i].strip()
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
        no = []
        yes = {}
        res_s = ""
        if len(lst) != 0:
            for i in res_d:
                if i == "":
                    return "Как будет называться ваш кошелёк?", {"bnk": res_d[i][0], "curr": res_d[i][1],
                                                                 "user_id": int(user_id)}
                else:
                    if len(from_db("accounts", "Accounts", {"user_id": int(user_id), "accounts": i})) == 0:
                        to_db("accounts", "Accounts", ("accounts", "bank", "currency"),
                              (i, res_d[i][0], res_d[i][-1]), int(user_id))
                        yes[i] = res_d[i]
                    else:
                        no.append(i)
            if len(no) > 0:
                if len(no) > 1:
                    r = random.randint(1, 2)
                    ll = [f"""Счета "{'", "'.join(no)}" уже существуют\n""",
                          f"""К сожалению, счета "{'", "'.join(no)}" уже существуют\n"""]
                    res_s += ll[r - 1]
                else:
                    r = random.randint(1, 3)
                    ll = [f'Счёт "{no[0]}" уже существует\n',
                          f'Увы :(\nСчёт "{no[0]}" уже существует\n',
                          f'Вы уже создали счёт "{no[0]}" ранее\n']
                    res_s += ll[r - 1]
            if len(yes) > 0:
                res_lst = []
                for k in yes:
                    if yes[k][1] != "тенге":
                        t = morph.parse(yes[k][1])[0]
                        res_lst.append(
                            f'"{k.capitalize()}" с суммой {yes[k][0]} {t.make_agree_with_number(yes[k][0]).word}\n')
                    else:
                        res_lst.append(f'"{k.capitalize()}" с суммой {yes[k][0]} {yes[k][1]}\n')
                if len(yes.keys()) > 1:
                    r = random.randint(1, 3)
                    ll = [f"Созданы счета:\n{''.join(res_lst)}\n",
                          f"Ура! Вы создали несколько счетов\n{''.join(res_lst)}\n",
                          f"Успешно созданы счета\n{''.join(res_lst)}\n"]
                    res_s += ll[r - 1]
                else:
                    r = random.randint(1, 3)
                    ll = [f"Создан счёт {''.join(res_lst)}\n",
                          f"Поздравляю!\nВы создали счёт {''.join(res_lst)}\n",
                          f"Новый счёт создан.\nЕго название {''.join(res_lst)}\n"]
                    res_s += ll[r - 1]
            return res_s.rstrip("\n"), {}
        else:
            return "Как будет называться ваш кошелёк?", {"bnk": 0, "curr": "рубль",
                                                                          "user_id": int(user_id)}
    elif len(k) > 0:
        req = req.lower()
        t = req.split()
        req = []
        for el in t:
            if el not in req_lst:
                req.append(el)
        req = " ".join(req)
        print(req)
        res_s = ""
        if len(from_db("accounts", "Accounts", {"user_id": k["user_id"], "accounts": req})) == 0:
            to_db("accounts", "Accounts", ("accounts", "currency", "bank"), (req, k["curr"], k["bnk"]), k["user_id"])
            r = random.randint(1, 3)
            t = morph.parse(k["curr"])[0]
            ress = f'"{req.capitalize()}" с суммой {k["bnk"]} {t.make_agree_with_number(int(k["bnk"])).word}\n'
            ll = [f"Создан счёт {req}\n",
                  f"Поздравляю!\nВы создали счёт {ress}\n",
                  f"Новый счёт создан.\nЕго название {ress}\n"]
            res_s += ll[r - 1]
        else:
            r = random.randint(1, 3)
            ll = [f'Счёт "{req}" уже существует\n',
                  f'Увы :(\nСчёт "{req}" уже существует\n',
                  f'Вы уже создали счёт "{req}" ранее\n']
            res_s += ll[r - 1]
        return res_s.rstrip("\n"), {}


def delete_wallet(req, user_ya_id, k=None):
    if k is None:
        k = {}
    if len(k) == 0:
        user_id = [i.id for i in from_db("users", "Users", {"username": user_ya_id})][0]
        req = req.lower().split()
        req_lst = ["олег", "закрой", "закрыть", "удали", "старый", "счет", "счёт", "счета", "кошелек", "кошелёк", "кошельки", "с",
                   "названием", "название", "названиями", "который", "которые", "называются",
                   "называется", "привет", "пожалуйста", "пока", "спасибо", "а", "ещё", "еще"]
        lst = []
        for it in req:
            if it not in req_lst:
                lst.append(it.strip(","))
        lst = " ".join(lst).split(" и ")
        no = []
        yes = []
        res_s = ""
        if "" not in lst:
            for i in lst:
                if len(from_db("accounts", "Accounts", {"accounts": i, "user_id": user_id})) == 0:
                    no.append(i)
                else:
                    prp = from_db("accounts", "Accounts", {"accounts": i, "user_id": user_id})[0].id
                    remove_from_db("waste", "Waste", {"account_id": prp})
                    remove_from_db("accounts", "Accounts", {"accounts": i, "user_id": user_id})
                    yes.append(i)
            if len(no) > 0:
                if len(no) > 1:
                    r = random.randint(1, 3)
                    ll = [f"""Счетов "{'", "'.join(no)}" не существует\n""",
                          f"""Счетов "{'", "'.join(no)}" не найдено\n""",
                          f"""Я не нашёл счетов "{'", "'.join(no)}"\n"""]
                    res_s += ll[r - 1]
                else:
                    r = random.randint(1, 3)
                    ll = [f'Счёта "{no[0]}" не существует\n',
                          f'Ой!\n Кажется, я не нашёл счёта "{no[0]}"\n',
                          f'Что-то не так!\n Счёта "{no[0]}" не существует\n']
                    res_s += ll[r - 1]
            if len(yes) > 0:
                if len(yes) > 1:
                    r = random.randint(1, 3)
                    ll = [f"""Счета "{'", "'.join(yes)}" были удалены\n""",
                          f"""Счета "{'", "'.join(yes)}" удалены успешно\n""",
                          f"""Счетов "{'", "'.join(yes)}" больше не существует\n"""]
                    res_s += ll[r - 1]
                else:
                    r = random.randint(1, 2)
                    ll = [f'Счёт "{yes[0]}" был удалён\n', f'Готово!\nЯ удалил счёт "{yes[0]}"\n']
                    res_s += ll[r - 1]
            return res_s.rstrip("\n"), {}
        else:
            return "Какой счёт я должен удалить?", {"user_id": int(user_id)}
    elif len(k) > 0:
        res_s = ""
        if len(from_db("accounts", "Accounts", {"accounts": req, "user_id": k["user_id"]})) == 0:
            r = random.randint(1, 3)
            ll = [f'Счёта "{req}" не существует\n',
                  f'Ой!\n Кажется, я не нашёл счёта "{req}"\n',
                  f'Что-то не так!\n Счёта "{req}" не существует\n']
            res_s += ll[r - 1]
        else:
            prp = from_db("accounts", "Accounts", {"accounts": req, "user_id": k["user_id"]})[0].id
            remove_from_db("waste", "Waste", {"account_id": prp})
            remove_from_db("accounts", "Accounts", {"accounts": req, "user_id": k["user_id"]})
            r = random.randint(1, 2)
            ll = [f'Счёт "{req}" был удалён\n', f'Готово!\nЯ удалил счёт "{req}"\n']
            res_s += ll[r - 1]
        return res_s.rstrip("\n"), {}
