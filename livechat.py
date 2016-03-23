import urllib.parse
import http.client

from flask import Flask, render_template, request

from celery import Celery

__all__ = ['app', 'base', 'livechat_ticket']

app = Flask(__name__)

app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@celery.task()
def google_analytics_task(data):
    for tag in data['chat']['tags']:
        params = urllib.parse.urlencode({
            'v': 1,
            'tid': 'UA-75377135-1',
            'cid': request.cookies.get('_GA'),
            't': 'event',
            'ec': 'LiveChat',
            'ea': tag,
            'el': data['chat'].get('id')
        })
        connection = http.client.HTTPConnection(
            'www.google-analytics.com')
        connection.request('POST', '/collect', params)
    return ""


@app.route('/', methods=['GET', 'POST'])
def base():
    return render_template('base.html')


@app.route('/livechat/ticket/', methods=['POST'])
def livechat_ticket():
    """ Send new track to Google analytic from LiveChatInc webhooks.
    (If "sales" is in chat tags)
    :return: ""
    """
    google_analytics_task.apply_async(request.json, countdown=30)
    return ""


if __name__ == '__main__':
    app.run(host='0.0.0.0')

