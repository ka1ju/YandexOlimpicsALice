# -*- coding: utf-8 -*-
import random
from skills.YandexOlympicsAlice.w2n
import pymorphy2
import requests
morph = pymorphy2.MorphAnalyzer()


def converter(text, k):
    try:
        sec_time = False
        req = text.lower().split()
        d = {'доллар': 'USD', 'доллара': 'USD', 'доллару': 'USD', 'долларом': 'USD', 'долларе': 'USD', 'доллары': 'USD',
             'долларов': 'USD', 'долларам': 'USD', 'долларами': 'USD', 'долларах': 'USD', 'евро': 'EUR',
             'рубль': 'RUB', 'рубля': 'RUB', 'рублю': 'RUB', 'рублём': 'RUB', 'рубле': 'RUB',
             'рубли': 'RUB', 'рублей': 'RUB', 'рублям': 'RUB', 'рублями': 'RUB', 'рублях': 'RUB', "тенге": "KZT",
             'юань': 'CNY', 'юаня': 'CNY', 'юаню': 'CNY', 'юанем': 'CNY', 'юане': 'CNY', 'юани': 'CNY',
             'юаней': 'CNY', 'юаням': 'CNY', 'юанями': 'CNY', 'юанях': 'CNY'}
        if len(k) == 0:
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
        else:
            sec_time = True
            res = []
            if "f_v" in k.keys():
                res.append(k["f_v"])
            else:
                res.append(d[text.lower()])
            if "summ" in k.keys():
                res.append(k["summ"])
            else:
                res.append(text.split()[0])
            if "s_v" in k.keys():
                res.append(k["s_v"])
            else:
                res.append(d[text.lower()])
        if not sec_time and (len(res) > 0 and True not in [x.isdigit() for x in res]):
            return "Какую сумму я должен перевести?", {"f_v": res[0], "s_v": res[1]}
        elif not sec_time and (len(res) > 0 and res[0].isdigit()):
            return "Из какой валюты я должен перевести?", {"s_v": res[0], "summ": res[1]}
        elif not sec_time and (len(res) > 0 and res[-1].isdigit()):
            return "В какую валюту я должен перевести?", {"f_v": res[0], "summ": res[1]}
        elif not sec_time and (len(res) > 3):
            return "Не понял вас, повторите", {}
        else:
            r1 = requests.get(f'https://ru.myfin.by/converter/{res[0].lower()}-{res[2].lower()}')
            r1 = r1.text
            r1 = r1[r1.find('<input id="to_input_curr" type="tel" value="') + 44::]
            r1 = r1[:r1.find('">')]
            exc_cur = {"евро": "евроцент", "рубль": "копейка", "доллар": "цент", "тенге": "тиын", "юань": "фынь"}
            d_from_abbr = {"RUB": "рубль", "EUR": "евро", 'USD': "доллар", "KZT": "тенге", "CNY": "юань"}
            for i in range(len(res)):
                if res[i].isalpha():
                    res[i] = d_from_abbr[res[i]]
            r = float(r1) * int(res[1])
            if res[2] != "тенге":
                w2 = morph.parse(res[2])[0].inflect({"datv"}).make_agree_with_number(int(float(r))).word
            else:
                w2 = res[2]
            if exc_cur[res[2]] != "тиын":
                lil_cur = morph.parse(exc_cur[res[2]])[0].inflect({"datv"}).make_agree_with_number(int(str(float(r) % 100)[str(float(r) % 100).find(".") + 1:str(float(r) % 100).find(".") + 3].lstrip("0"))).word
            else:
                if int(res[1]) == 0:
                    lil_cur = "тиынам"
                elif int(res[1]) == 1:
                    lil_cur = "тиыну"
                else:
                    lil_cur = "тиынам"
            if int(res[1]) == 0:
                rav = "равно"
            elif int(res[1]) == 1:
                rav = "равен"
            else:
                rav = "равны"
            if res[0] != "тенге":
                w1 = morph.parse(res[0])[0].make_agree_with_number(int(res[1])).word
            else:
                w1 = res[0]
            x = random.randint(0, 2)
            rand = ["Давайте посчитаем...", "По нынешнему курсу", "По моим подсчётам"]
            ress = ""
            if int(float(r)) != 0:
                ress += f" {int(float(r))} {w2}"
            if int(str(float(r) % 100)[str(float(r) % 100).find(".") + 1:str(float(r) % 100).find(".") + 3].lstrip("0")) != 0:
                ress += f' {str(float(r) % 100)[str(float(r) % 100).find(".") + 1:str(float(r) % 100).find(".") + 3].lstrip("0")} {lil_cur}'
            return f'{rand[x]}\n{res[1]} {w1} примерно {rav}{ress}', {}
    except Exception as e:
        print("ERROR converter", e)
        return "Увы :(\nМеня не научили переводить такое", {}
