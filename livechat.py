import requests
import urllib.parse

from flask import Flask, render_template, request
import http.client
from celery import Celery

__all__ = ['app', 'base', 'livechat_ticket']

app = Flask(__name__)

app.config.update(
    CELERY_BROKER_URL='redis://0.0.0.0:6379',
    CELERY_RESULT_BACKEND='redis://0.0.0.0:6379',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json'
)
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@celery.task()
def google_analytics_task(data, ga):
    auth = ('kidomakai@gmail.com', 'd68ed9aac8511fedb315199228bfb03c')
    url = 'https://api.livechatinc.com/chats/'+data['chat']['id']+'/'
    headers = {"X-API-Version": "2"}
    request_data = requests.get(url, headers=headers, auth=auth)

    for tag in request_data.json()['tags']:
        params = urllib.parse.urlencode({
            'v': 1,
            'tid': 'UA-75377135-1',
            'cid': ga,
            't': 'event',
            'ec': 'LiveChat',
            'ea': tag,
            'el': data['chat']['id']
        })
        connection = http.client.HTTPConnection(
            'www.google-analytics.com')
        connection.request('POST', '/collect', params)


@app.route('/', methods=['GET', 'POST'])
def base():
    return render_template('base.html')


@app.route('/livechat/ticket/', methods=['POST'])
def livechat_ticket():
    """ Send new track to Google analytic from LiveChatInc webhooks.
    (If "sales" is in chat tags)
    :return: ""
    """

    google_analytics_task.apply_async((request.json, request.cookies.get('_GA')), countdown=3)
    return ""


if __name__ == '__main__':
    app.run(host='0.0.0.0')

