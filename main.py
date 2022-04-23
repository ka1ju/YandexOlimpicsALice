from flask import Flask, request
import logging
import json
from funcs import out
from oleg import *

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)


@app.route('/', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')

    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    handle_dialog(request.json, response)
    logging.info(f'Response:  {response!r}')
    return json.dumps(response)


def handle_dialog(req, res):
    user_id = req['session']['user_id']
    user_message = req['request']['command'].lower()

    if req['session']['new']:
        res['response']['text'] = authorization(user_id)
        return

    if ('созд' in user_message or 'доб' in user_message) and \
            ('кошел' in user_message or 'счёт' in user_message):
        res['response']['text'] = "Хорошо, создадим кошелёк"
        return

    if ('удал' in user_message or 'убр' in user_message) and \
            ('кошел' in user_message or 'счёт' in user_message):
        res['response']['text'] = "Подтвердите удаление кошелька"
        return

    if ('пополн' in user_message or 'зачисл' in user_message) and \
            ('кошел' in user_message or 'счёт' in user_message):
        res['response']['text'] = "Пополнил кошелёк"
        return

    if ('трат' in user_message or 'сн' in user_message) and \
            ('кошел' in user_message or 'счёт' in user_message):
        res['response']['text'] = "Снял с кошелька"
        return

    if ('выв' in user_message or 'дай' in user_message or 'ска' in user_message) and \
            'инф' in user_message and \
            ('кошел' in user_message or 'счёт' in user_message):
        res['response']['text'] = "Вывел информацию о счёте"
        return

    if ('выв' in user_message or 'дай' in user_message or 'ска' in user_message) and \
            'стат' in user_message:
        res['response']['text'] = "Вывел статистику"
        return

    res['response']['text'] = "Извините, я Вас не понял."


if __name__ == '__main__':
    app.run(port=5000)

# C:\Users\Administrator\Desktop\ngrok http 5000
