from flask import *
import logging
import json

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)


@app.route('/', methods=["POST"])
def hello():
    logging.info(request.json)

    response = \
        {
            "version": request.json["version"],
            "session": request.json["session"],
            "response":
                {
                    "end_session": False
                }
        }
    req = request.json
    if req["session"]["new"]:
        response["response"]["text"] = "Salam."

    return json.dumps(response)