import json


def helper():
    inp = json.load(open('funcs.json', mode='r', encoding="utf-8"))
    return "Вот что я умею:\n" + '\n'.join([i for i in inp]) + '.\nТакже, если вы хотите завершить диалог со мной,' \
                                                               ' то можете ответить мне спасибо.'
