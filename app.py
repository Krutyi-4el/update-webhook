from flask import Flask, request
from waitress import serve
from discord import (
    Embed,
    Webhook,
    RequestsWebhookAdapter,  # also need `requests`
    Color
)
from os import getenv
from json import loads
from datetime import datetime


app = Flask(__name__)
processed = []


@app.route('/webhook', methods=['POST'])
def test():
    print(request.data, request.args)
    if request.args.get('token', None) != getenv("AUTHORIZATION_CODE"):
        return "authorization required", 401
    data = loads(request.data)
    if data["data"]["id"] in processed:
        return "ok, already done"
    processed.append(data["data"]["id"])
    success = data["data"]["status"] == "succeeded"
    embed = Embed(
        title="Обновление",
        description="Программа обновлена" if success else "Ошибка",
        color=Color.green() if success else Color.red(),
        timestamp=datetime.fromisoformat(
            data["published_at"].replace("Z", "+00:00")
        )
    )
    embed.add_field(
        name="Версия",
        value=data["data"]["version"],
        inline=False
    )
    embed.add_field(
        name="Описание",
        value=data["data"]["description"],
        inline=False
    )
    Webhook.from_url(
        getenv("WEBHOOK_URL"),
        adapter=RequestsWebhookAdapter()
    )
    .send(embed=embed)
    return "ok"


if __name__ == '__main__':
    serve(app, port=getenv("PORT"))
