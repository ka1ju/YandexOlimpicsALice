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
        res['response']['text'] = hello()
        return

    if ('создать' in req['session']['text'] or 'добавить' in req['session']['text']) and \
            ('кошелёк' in req['session']['text'] or 'счёт' in req['session']['text']):
        pass

    elif ('удалить' in req['session']['text'] or 'убрать' in req['session']['text']) and \
            ('кошелёк' in req['session']['text'] or 'счёт' in req['session']['text']):
        pass

    elif ('пополнить' in req['session']['text'] or 'зачислить' in req['session']['text']) and \
            ('кошелёк' in req['session']['text'] or 'счёт' in req['session']['text']):
        pass

    elif ('потратить' in req['session']['text'] or 'зачислить' in req['session']['text']) and \
            ('кошелёк' in req['session']['text'] or 'счёт' in req['session']['text']):
        pass

    res['response']['text'] = "hmm"


def hello():
    return "Привет, меня зовут Олег. Я создан для того чтобы вести учёт ваших трат. Вот краткий список моих функций:\n" \
           + out()


if __name__ == '__main__':
    app.run(port=5000)

# C:\Users\Administrator\Desktop\ngrok http 5000
