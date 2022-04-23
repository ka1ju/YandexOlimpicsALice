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
    if req['session']['new']:
        res['response']['text'] = autorization(user_id)
        return

    if ('созд' in req['request']['command'] or 'доб' in req['request']['command']) and \
            ('кошел' in req['request']['command'] or 'счёт' in req['request']['command']):
        res['response']['text'] = "Хорошо, создадим кошелёк"
        return

    if ('удал' in req['request']['command'] or 'убр' in req['request']['command']) and \
            ('кошел' in req['request']['command'] or 'счёт' in req['request']['command']):
        res['response']['text'] = "Подтвердите удаление кошелька"
        return

    if ('пополн' in req['request']['command'] or 'зачисл' in req['request']['command']) and \
            ('кошел' in req['request']['command'] or 'счёт' in req['request']['command']):
        res['response']['text'] = "Пополнил кошелёк"
        return

    if ('трат' in req['request']['command'] or 'сн' in req['request']['command']) and \
            ('кошел' in req['request']['command'] or 'счёт' in req['request']['command']):
        res['response']['text'] = "Снял с кошелька"
        return

    if True:
        pass

    res['response']['text'] = "Извините, я Вас не понял."


if __name__ == '__main__':
    app.run(port=5000)

# C:\Users\Administrator\Desktop\ngrok http 5000
