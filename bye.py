import random
import json


def bye():
    answers = ["До свидания", "Пока", "Увидимся."]
    inp = open("prev_alice_message.json", "r", encoding="utf-8")
    mess = json.load(inp)
    inp.close()
    out = open("prev_alice_message.json", 'w', encoding="utf-8")
    if mess['prev_bye'] in answers:
        answers.remove(mess['prev_bye'])
    index = random.randint(0, len(answers) - 1)
    answer = answers[index]
    mess['prev_hello'] = answer
    json.dump(mess, out)
    return answer
