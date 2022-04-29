# -*- coding: utf-8 -*-
import random

import w2n
import pymorphy2
import requests

morph = pymorphy2.MorphAnalyzer()


def converter(text):
    try:
        req = text.lower().split()
        d = {'доллар': 'USD', 'доллара': 'USD', 'доллару': 'USD', 'долларом': 'USD', 'долларе': 'USD', 'доллары': 'USD',
             'долларов': 'USD', 'долларам': 'USD', 'долларами': 'USD', 'долларах': 'USD', 'евро': 'EUR',
             'рубль': 'RUB', 'рубля': 'RUB', 'рублю': 'RUB', 'рублём': 'RUB', 'рубле': 'RUB',
             'рубли': 'RUB', 'рублей': 'RUB', 'рублям': 'RUB', 'рублями': 'RUB', 'рублях': 'RUB', "тенге": "KZT",
             'юань': 'CNY', 'юаня': 'CNY', 'юаню': 'CNY', 'юанем': 'CNY', 'юане': 'CNY', 'юани': 'CNY',
             'юаней': 'CNY', 'юаням': 'CNY', 'юанями': 'CNY', 'юанях': 'CNY'}
        lst = []
        for i in range(len(req)):
            try:
                parse_it = morph.parse(req[i])
                maybe_num = parse_it[0].normal_form
                req[i] = str(w2n.word_to_num(maybe_num))
            except Exception:
                pass
        for i in req:
            if i.isdigit():
                lst.append(str(i))
            elif i == "в":
                lst.append(i)
            elif i in d.keys() and d[i] not in lst:
                lst.append(d[i])
        flag = False
        res = []
        is_strange = False
        is_strange_v = False
        c = False
        if "сколько" in req:
            for i in lst:
                if i == "в":
                    flag = True
                    c = True
                    if len(res) == 0:
                        is_strange_v = True
                elif i.isalpha() and not flag:
                    res.append(i)
                elif i.isalpha() and flag:
                    res.insert(0, i)
                    flag = False
                if i.isdigit() and len(res) == 1 and c:
                    is_strange = True
        elif "переведи" in req:
            for i in lst:
                if i == "в":
                    flag = True
                    c = True
                    if len(res) == 0:
                        is_strange_v = True
                elif i.isalpha() and flag:
                    res.append(i)
                elif i.isalpha() and not flag:
                    res.insert(0, i)
                if i.isdigit() and len(res) == 1 and c:
                    is_strange = True
        for it in lst:
            if it.isdigit():
                res.insert(1, it)
        if is_strange and is_strange_v:
            res = res[::-1]
        r = requests.get(f'https://ru.myfin.by/converter/{res[0].lower()}-{res[2].lower()}/{res[1]}')
        r = r.text
        r = r[r.find('<input id="to_input_curr" type="tel" value="') + 44::]
        r = r[:r.find('">')]

        r1 = requests.get(f'https://ru.myfin.by/converter/{res[0].lower()}-{res[2].lower()}')
        r1 = r1.text
        r1 = r1[r1.find('<input id="to_input_curr" type="tel" value="') + 44::]
        r1 = r1[:r1.find('">')]
        d_from_abbr = {"RUB": "рубль", "EUR": "евро", 'USD': "доллар", "KZT": "тенге", "CNY": "юань"}
        for i in range(len(res)):
            if res[i].isalpha():
                res[i] = d_from_abbr[res[i]]
        if res[2] != "тенге":
            w2 = morph.parse(res[2])[0].make_agree_with_number(round(float(r), 2)).inflect({"datv"}).word
        else:
            w2 = res[2]
            r = float(r1) * int(res[1])
        if res[0] != "тенге":
            w1 = morph.parse(res[0])[0].make_agree_with_number(int(res[1])).word
        else:
            w1 = res[0]
        x = random.randint(0, 2)
        rand = ["Давайте посчитаем...", "По нынешнему курсу", "По моим подсчётам"]
        return f'{rand[x]}\n{res[1]} {w1} равно {round(float(r), 2)} {w2}'
    except Exception:
        return "Не понял вас, повторите"
