from flask import Flask, request
import logging
import json
from funcs import out

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

    a = ''

    if req['session']['new']:
        a = hello(0)
        pass

    if req['request']['original_utterance'].lower() in [
        'ладно',
        'куплю',
        'покупаю',
        'хорошо'
    ]:
        res['response']['text'] = 'Слона можно найти на Яндекс.Маркете!'
        res['response']['end_session'] = True
        return

    res['response']['text'] = a
    return


def hello(req):
    return "Привет, меня зовут Олег. Я создан для того чтобы вести учёт ваших трат. Вот краткий список моих функций:\n" \
           + out()


if __name__ == '__main__':
    app.run(port=5000)

# C:\Users\Administrator\Desktop\ngrok http 5000
