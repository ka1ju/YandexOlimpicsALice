import random


def bye(prev):
    answers = ["До свидания", "Пока", "Увидимся", "До встречи"]
    if 'session' in prev:
        if 'bye' in prev['session']:
            answers.remove(prev['session']['bye'])
    return answers[random.randint(0, len(answers) - 1)]
