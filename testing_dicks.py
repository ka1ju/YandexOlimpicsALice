import flask
from flask import Flask, request, session
import requests
import logging
import json
from funcs import out
from oleg import *
from all_wallets import *
from create_delete_wallet import *
from flask import Flask, request, jsonify, redirect
from requests import post
import sys

if sys.version_info < (3, 0):  # Pytohn2.x
    from urllib import urlencode
else:  # Python3.x
    from urllib.parse import urlencode
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

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


    return json.dumps({
    "start_account_linking": {},
    "version": "1.0"
    })


@app.route('/getting', methods=['POST', 'GET'])
def getting():
    code = request.values.to_dict()['code']
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': 'bd45522bdc974905a993b3666e87e79c',
        'client_secret': '615c67d59a2c4b95a8ddb7dd774475aa'
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
    return flask.redirect(f'https://social.yandex.net/broker/redirect?state={statuation}&client_id={client_id}&scope={scope}&code={code}&response_type=code')


@app.route('/login', methods=['POST', 'GET'])
def login():
    statuation = request.args.get('state')
    client_id = request.args.get('client_id')
    scope = request.args.get('scope')
    session['statuation'] = statuation
    session['client_id'] = client_id
    session['scope'] = scope
    return flask.redirect(f'https://oauth.yandex.ru/authorize?response_type=code&client_id=bd45522bdc974905a993b3666e87e79c&redirect_uri=https://da04-94-180-1-142.eu.ngrok.io/code_get')


if __name__ == '__main__':
    app.run(port=5000)
