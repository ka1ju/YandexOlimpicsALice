import random
import json


def thanks():
    answers = ["Не за что 😅", "Пожалуйста 👍", "Обращайтесь 😃"]
    inp = open("prev_alice_message.json", "r", encoding="utf-8")
    mess = json.load(inp)
    inp.close()
    out = open("prev_alice_message.json", 'w', encoding="utf-8")
    if mess['prev_thanks'] in answers:
        answers.remove(mess['prev_thanks'])
    index = random.randint(0, len(answers) - 1)
    answer = answers[index]
    mess['prev_thanks'] = answer
    json.dump(mess, out)
    return answer
