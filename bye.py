import random
import json


def bye():
    answers = ["Здравствуйте, чем могу помочь?", "Привет, чем помочь? 👍", "Здравствуйте, чем могу быть полезен? 😃"]
    inp = open("prev_alice_message.json", "r", encoding="utf-8")
    mess = json.load(inp)
    inp.close()
    out = open("prev_alice_message.json", 'w', encoding="utf-8")
    if mess['prev_bye'] in answers:
        answers.remove(mess['prev_bye'])
    answer = random.choice(answers)
    mess['prev_hello'] = answer
    json.dump(mess, out)
    return answer
