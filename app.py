from flask import Flask, request
from waitress import serve
from discord import Webhook, RequestsWebhookAdapter  # also need `requests`
from os import getenv
from json import loads


app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def test():
    print(request.form, request.args)
    if request.args.get('token', None) != getenv("AUTHORIZATION_CODE"):
        return "authorization required", 401
    w = Webhook.from_url(
        getenv("WEBHOOK_URL"),
        adapter=RequestsWebhookAdapter()
    )
    w.send(loads(request.form['data'])['version'])
    return "ok"


if __name__ == '__main__':
    serve(app, port=getenv("PORT"))
