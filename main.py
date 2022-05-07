from helper import *
from thanks import *
from hello import *
from bye import *
from oleg import *
from all_wallets import *
from create_delete_wallet import *
from top_up_wallet import *
from wasting2 import *
from converter import *
from Info_Alise_3 import *
from flask import Flask, request, redirect, session
from requests import post
from urllib.parse import urlencode
import flask
import logging
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ИДИ НАХУЙ'

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
logging.basicConfig(level=logging.INFO)
funcs_as_json = json.load(open('funcs.json', mode='r', encoding="utf-8"))


@app.route('/', methods=['POST'])
def main():
    print()
    logging.info(f'Request: {request.json!r}')

    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        },
        'session_state': {
            'create_wallet': {},
            'delete_wallet': {},
            'top_up_wallet': {},
            'spend_money': {},
            'wallet_info': {},
            'wallet_statistic': {},
            'all_wallets': {},
            'transfer': {}
        }
    }
    if "session" in request.json['state']:
        if 'bye' in request.json['state']['session']:
            response['session_state']['bye'] = request.json['state']['session']['bye']
        if 'hello' in request.json['state']['session']:
            response['session_state']['hello'] = request.json['state']['session']['hello']
        if 'thanks' in request.json['state']['session']:
            response['session_state']['thanks'] = request.json['state']['session']['thanks']
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
    if 'request' in req:
        user_message = req['request']['command'].lower()

        # Помощь
        if "помо" in user_message or ("что" in user_message and "ты" in user_message and "умеешь" in user_message):
            res['response']['text'] = helper(funcs_as_json)
            res['session_state'] = req['state']['session']
            for i in res['session_state']:
                if i not in ['bye', "hello," "thanks"]:
                    res['session_state'][i] = {}
            logging.info("Helping")
            return

        if "отмен" in user_message:
            res['response']['text'] = "Текущая операция отменена"
            for i in res['session_state']:
                if i not in ['bye', "hello," "thanks"]:
                    res['session_state'][i] = {}
            logging.info("Cancelling")
            return

        # Авторизация
        if req['session']['new'] and user_message == "":
            res['response']['text'] = authorization(user_id, funcs_as_json)
            logging.info("Authorising user")
            return

        # Создание кошелька
        if (('созд' in user_message or 'откр' in user_message) and
            ('кошел' in user_message or 'счет' in user_message or 'счёт' in user_message)) \
                or req['state']['session']['create_wallet'] != {}:
            res['response']['text'], res['session_state']['create_wallet'] = \
                create_wallet(user_message, user_id, req['state']['session']['create_wallet'])
            logging.info("Adding wallet")
            return

        # Удаление кошелька
        if ('удал' in user_message or 'убр' in user_message or 'закр' in user_message) and \
                ('кошел' in user_message or 'счет' in user_message or 'счёт' in user_message) \
                or req['state']['session']['delete_wallet'] != {}:
            res['response']['text'], res['session_state']['delete_wallet'] = \
                delete_wallet(user_message, user_id, req['state']['session']['delete_wallet'])
            logging.info("Deleting wallet")
            return

        # Пополнение кошелька
        if (('пополн' in user_message or 'зачисл' in user_message or "доб" in user_message or "полож" in user_message) and
            ('кошел' in user_message or 'счет' in user_message or 'счёт' in user_message)) \
                or req['state']['session']['top_up_wallet'] != {}:
            res['response']['text'], res['session_state']['top_up_wallet'] = \
                top_up_wallet(user_message, user_id, req['state']['session']['top_up_wallet'])
            logging.info("Topping wallet up")
            return

        # Снятие денег или трата денег с кошелька
        if ('трат' in user_message or 'сн' in user_message or "спи" in user_message) and \
                ('кошел' in user_message or 'счет' in user_message or 'счёт' in user_message) \
                or req['state']['session']['spend_money'] != {}:
            res['response']['text'], res['session_state']['spend_money'] = \
                wasting(user_message, user_id, req['state']['session']['spend_money'])
            logging.info("Spending money")
            return

        # Вывод информации о счёте
        if ('балан' in user_message or 'инф' in user_message) and \
                ('кошел' in user_message or 'счет' in user_message or 'счёт' in user_message) \
                or req['state']['session']['wallet_info'] != {}:
            res['response']['text'], res['session_state']['wallet_info'] = \
                information(user_message, user_id, req['state']['session']['wallet_info'])
            logging.info("Giving info about wallet")
            return

        # Вывод статистики о счёте
        if 'стат' in user_message or req['state']['session']['wallet_statistic'] != {}:
            res['response']['text'], res['session_state']['wallet_statistic'] = \
                statistic(user_message, user_id, req['state']['session']['wallet_statistic'])
            logging.info("Giving wallet statistic")
            return

        # Вывод всех кошельков
        if ('выв' in user_message or 'дай' in user_message or 'ска' in user_message or "покаж" in user_message
            or "показ" in user_message) and \
                ('кошел' in user_message or 'счет' in user_message):
            res['response']['text'] = res['session_state']['all_wallets'] = return_wallets(user_id, req['state'])
            logging.info("Giving all wallets")
            return

        # Конвертация валют
        if 'конверт' in user_message or 'перев' in user_message or ("сколько" in user_message and "в" in user_message):
            res['response']['text'], res['session_state']['transfer'] = \
                converter(user_message, req['state']['session']['transfer'])
            logging.info("Converting")
            return

        # Ответ на благодарность
        if "спасибо" in user_message or "благодар" in user_message or "спс" in user_message:
            res['response']['text'] = res['session_state']['thanks'] = thanks(req['state'])
            res['response']['end_session'] = True
            logging.info("Saying 'Thanks'")
            return

        # Ответ на приветствие
        if "привет" in user_message or "здорово" in user_message or "хай" in user_message:
            res['response']['text'] = res['session_state']['hello'] = hello(req['session']['message_id'], req['state'])
            logging.info("Saying 'Hello'")
            return

        # Ответ на прощание
        if "до свидания" in user_message or "пока" in user_message or "прощай" in user_message:
            res['response']['text'] = res['session_state']['bye'] = bye(req['state'])
            res['response']['end_session'] = True
            logging.info("Saying 'Bye'")
            return

        res['response']['text'] = "Извините, я Вас не понял."
        logging.info("Bot unknown question")
        return
    else:
        print(req)
        res['response']['text'] = authorization(req['session']['user']['access_token'], funcs_as_json)
        logging.info("Authorising user")
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
    st = session.get('st', None)
    client_id = session.get('client_id', None)
    scope = session.get('scope', None)
    return redirect(
        f'https://social.yandex.net/broker/redirect?state={st}&client_id={client_id}&scope={scope}&code={code}')


@app.route('/login', methods=['POST', 'GET'])
def login():
    st = request.args.get('state')
    client_id = request.args.get('client_id')
    scope = request.args.get('scope')
    session['st'] = st
    session['client_id'] = client_id
    session['scope'] = scope
    return flask.redirect(
        f'https://oauth.yandex.ru/authorize?response_type=code&client_id=eb2919ba420a467d9f9d958096364a97&redirect_uri=https://a648-93-91-160-93.in.ngrok.io/code_get')


if __name__ == '__main__':
    app.run(port=6000)

# cd C:\Users\Ярослав\OneDrive\Рабочий стол .\ngrok http 6000
