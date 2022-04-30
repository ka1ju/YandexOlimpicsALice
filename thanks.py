import random


def thanks(prev):
    answers = ["Не за что 😅.", "Пожалуйста 👍.", "Обращайтесь 😃."]
    if 'session' in prev:
        if 'thanks' in prev['session']:
            answers.remove(prev['session']['thanks'])
    return answers[random.randint(0, len(answers) - 1)]
