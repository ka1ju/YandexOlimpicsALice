import flask
from flask import Flask, request
import requests
import logging
import json
from funcs import out
from oleg import *
from all_wallets import *
from create_delete_wallet import *
from flask import Flask, request, jsonify, redirect
from requests import post

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


    return json.dumps({
    "start_account_linking": {},
    "version": "1.0"
    })


@app.route('/getting', methods=['POST', 'GET'])
def getting():
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': 'bd45522bdc974905a993b3666e87e79c',
        'client_secret': '615c67d59a2c4b95a8ddb7dd774475aa'
    }
    data = urlencode(data)
    print(code)
    baseurl = 'https://oauth.yandex.ru/'
    k = post(baseurl + "token", data).json()
    print(k)
    return json.dumps(k)


@app.route('/code_get', methods=['POST', 'GET'])
def code_get():
    global code
    code = request.args.get('code')
    return redirect(f'https://social.yandex.net/broker/redirect?state={statuation}&client_id={client_id}&scope={scope}&code={code}')


@app.route('/login', methods=['POST', 'GET'])
def login():
    global statuation, client_id, scope
    statuation = request.args.get('state')
    client_id = request.args.get('client_id')
    scope = request.args.get('scope')
    return flask.redirect(f'https://oauth.yandex.ru/authorize?response_type=code&client_id=bd45522bdc974905a993b3666e87e79c&redirect_uri=https://248c-94-180-1-142.eu.ngrok.io/code_get')


if __name__ == '__main__':
    app.run(port=5000)