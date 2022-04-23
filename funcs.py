import json


def out():
    f = open('funcs.json', 'r', encoding='utf-8')
    x = json.load(f)
    output = [""]
    for i in x:
        output.append(i)
    return "\n".join(output)