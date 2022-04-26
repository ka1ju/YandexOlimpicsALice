import random
import json


def hello(mess_id):
    if mess_id == 0:
        answers = ["Здравствуйте, чем могу помочь?", "Привет, чем помочь? 👍", "Здравствуйте, чем могу быть полезен? 😃"]
        inp = open("prev_alice_message.json", "r", encoding="utf-8")
        mess = json.load(inp)
        inp.close()
        out = open("prev_alice_message.json", 'w', encoding="utf-8")
        if mess['prev_hello'] in answers:
            answers.remove(mess['prev_hello'])
        index = random.randint(0, len(answers) - 1)
        answer = answers[index]
        mess['prev_hello'] = answer
        json.dump(mess, out)
        return answer
    else:
        answers = ["Мы уже здоровались :)", "Мы здороваемся не первый раз :)"]
        inp = open("prev_alice_message.json", "r", encoding="utf-8")
        mess = json.load(inp)
        inp.close()
        out = open("prev_alice_message.json", 'w', encoding="utf-8")
        if mess['prev_already_hello'] in answers:
            answers.remove(mess['prev_already_hello'])
        index = random.randint(0, len(answers) - 1)
        answer = answers[index]
        mess['prev_hello'] = answer
        json.dump(mess, out)
        return answer
