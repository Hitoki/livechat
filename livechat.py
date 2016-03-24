import requests
import urllib.parse
import http.client

from flask import Flask, render_template, request

from celery import Celery

__all__ = ['app', 'celery', 'google_analytics_task',
           'base', 'livechat_ticket']

app = Flask(__name__)

app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379/0',
    CELERY_RESULT_BACKEND='redis://localhost:6379/0',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json'
)

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@celery.task()
def google_analytics_task(data, ga):
    """ Celery task, send Google statistics

    :param data: JSON request data from LiveChat webhook
    :type data: dict
    :param ga: Request cookie User ID
    :type ga: str
    :return: ""
    """
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
    return ""


@app.route('/', methods=['GET', 'POST'])
def base():
    """ Base endpoint, for display LiveChat
    :return: "template: base.html"
    """
    return render_template('base.html')


@app.route('/livechat/ticket/', methods=['GET', 'POST'])
def livechat_ticket():
    """ Send new track to Google analytic from LiveChatInc webhooks endpoint.
    :return: ""
    """
    google_analytics_task.apply_async(
        args=(request.get_json(), request.cookies.get('_GA')), countdown=30)
    # livechat.google_analytics_task.apply_async(args=({'chat':{'id':'12312','tags':['test']}}, '123.123'), countdown=30)
    return ""


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

