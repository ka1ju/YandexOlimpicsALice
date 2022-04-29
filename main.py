from helper import *
from thanks import *
from hello import *
from bye import *
from oleg import *
from all_wallets import *
from create_delete_wallet import *
import flask
from flask import Flask, request, redirect, session
from requests import post
from converter import *
from urllib.parse import urlencode
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ИДИ НАХУЙ'

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

    if request.json['session']['new'] and "access_token" not in request.json['session']['user']:
        return json.dumps({
            "start_account_linking": {},
            "version": "1.0"
        })

    handle_dialog(request.json, response)
    logging.info(f'Response:  {response!r}')
    return json.dumps(response)


def handle_dialog(req, res):
    user_id = req['session']['user']['access_token']
    try:
        user_message = req['request']['original_utterance'].lower()

        # Авторизация
        if req['session']['new'] and user_message == "":
            res['response']['text'] = authorization(user_id)
            logging.info("Authorising user")
            return

        # Создание кошелька
        if ('созд' in user_message or 'доб' in user_message) and \
                ('кошел' in user_message or 'счет' in user_message or 'счёт' in user_message):
            res['response']['text'] = create_wallet(user_message, user_id)
            logging.info("Adding wallet")
            return

        # Удаление кошелька
        if ('удал' in user_message or 'убр' in user_message) and \
                ('кошел' in user_message or 'счет' in user_message or 'счёт' in user_message):
            res['response']['text'] = delete_wallet(user_message, user_id)
            logging.info("Deleting wallet")
            return

        # Пополнение кошелька
        if ('пополн' in user_message or 'зачисл' in user_message) and \
                ('кошел' in user_message or 'счет' in user_message or 'счёт' in user_message):
            res['response']['text'] = "Пополнил кошелёк"
            logging.info("Adding money")
            return

        # Снятие денег или трата денег с кошелька
        if ('трат' in user_message or 'сн' in user_message) and \
                ('кошел' in user_message or 'счет' in user_message or 'счёт' in user_message):
            res['response']['text'] = "Снял с кошелька"
            logging.info("Spending money")
            return

        # Вывод информации о счёте
        if ('выв' in user_message or 'дай' in user_message or 'ска' in user_message) and \
                'инф' in user_message and \
                ('кошел' in user_message or 'счет' in user_message or 'счёт' in user_message):
            res['response']['text'] = "Вывел информацию о счёте"
            logging.info("Giving info about wallet")
            return

        # Вывод статистики о счёте
        if ('выв' in user_message or 'дай' in user_message or 'ска' in user_message) and \
                'стат' in user_message:
            res['response']['text'] = statistic(user_message, user_id)
            logging.info("Giving statics about expenses")
            return

        # Вывод всех кошельков
        if ('выв' in user_message or 'дай' in user_message
            or 'ска' in user_message or "покаж" in user_message
            or "показ" in user_message) and \
                ('кошел' in user_message or 'счет' in user_message):
            res['response']['text'] = return_wallets(user_id)
            logging.info("Giving all wallets")
            return

        # Конвертация валют
        if 'конверт' in user_message or 'перев' in user_message or ("сколько" in user_message and "в" in user_message):
            res['response']['text'] = converter(user_message)
            return

        # Помощь
        if "помо" in user_message or ("что" in user_message and "ты" in user_message and "умеешь" in user_message):
            res['response']['text'] = helper()
            return

        # Ответ на благодарность
        if "спасибо" in user_message or "благодар" in user_message or "спс" in user_message:
            res['response']['text'] = thanks()
            res['response']['end_session'] = True
            return

        # Ответ на приветствие
        if "привет" in user_message or "здорово" in user_message or "хай" in user_message:
            res['response']['text'] = hello(req['session']['message_id'])
            return

        # Ответ на прощание
        if "до свидания" in user_message or "пока" in user_message or "прощай" in user_message:
            res['response']['text'] = bye()
            res['response']['end_session'] = True
            return

        res['response']['text'] = "Извините, я Вас не понял."
    except KeyError:
        print(req)
        res['response']['text'] = authorization(req['session']['user']['access_token'])
        return


# ТУТ НАЧИНАЕТСЯ ПИЗДА, ПОЭТОМУ НЕ ЛЕЗЬ А ТО ВЫЕБУ КТО БЫ ТЫ НИ БЫЛ.


@app.route('/getting', methods=['POST', 'GET'])
def getting():
    code = request.values.to_dict()['code']
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': 'eb2919ba420a467d9f9d958096364a97',
        'client_secret': '445686f67ceb472dad8c77d0631e74f9'
    }
    data = urlencode(data)
    baseurl = 'https://oauth.yandex.ru/'
    k = post(baseurl + "token", data).json()
    return json.dumps(k)


@app.route('/code_get', methods=['POST', 'GET'])
def code_get():
    code = request.args.get('code')
    session['code'] = code
    statuation = session.get('statuation', None)
    client_id = session.get('client_id', None)
    scope = session.get('scope', None)
    return redirect(
        f'https://social.yandex.net/broker/redirect?state={statuation}&client_id={client_id}&scope={scope}&code={code}')


@app.route('/login', methods=['POST', 'GET'])
def login():
    statuation = request.args.get('state')
    client_id = request.args.get('client_id')
    scope = request.args.get('scope')
    session['statuation'] = statuation
    session['client_id'] = client_id
    session['scope'] = scope
    return flask.redirect(
        f'https://oauth.yandex.ru/authorize?response_type=code&client_id=eb2919ba420a467d9f9d958096364a97&redirect_uri=https://0152-5-137-125-18.eu.ngrok.io/code_get')


if __name__ == '__main__':
    app.run(port=6000)

# cd C:\Users\Ярослав\OneDrive\Рабочий стол .\ngrok http 6000
