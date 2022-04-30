import random


def hello(mess_id, prev):
    if mess_id == 0:
        answers = ["Здравствуйте, чем могу помочь?.", "Привет, чем помочь? 👍.",
                   "Здравствуйте, чем могу быть полезен? 😃."]
        if 'session' in prev:
            if 'hello' in prev['session']:
                answers.remove(prev['session']['hello'])
        return answers[random.randint(0, len(answers) - 1)]
    else:
        answers = ["Мы уже здоровались :)", "Мы здороваемся не первый раз :)"]
        if 'session' in prev:
            if 'hello' in prev['session']:
                answers.remove(prev['session']['hello'])
        return answers[random.randint(0, len(answers) - 1)]
