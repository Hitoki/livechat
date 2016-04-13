import requests
import urllib.parse
import http.client

from celery import Celery

from livechat import app
from livechat.models import User


app.config.update(
    BROKER_URL='redis://localhost:6379/0',
    CELERY_RESULT_BACKEND='redis://localhost:6379/0',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json'
)


from raven import Client
from raven.contrib.celery import register_signal, register_logger_signal
from raven.contrib.flask import Sentry


class Celery(Celery):

    def on_configure(self):
        client = Client('https://368294fb0e6e4739861c08a2bc277212:b25295a8dcb74cdf98ed95dea61ef2e0@app.getsentry.com/71566')

        # register a custom filter to filter out duplicate logs
        register_logger_signal(client)

        # hook into the Celery error handler
        register_signal(client)

celery = Celery(app.name)
celery.conf.update(app.config)

sentry = Sentry(app, dsn='https://368294fb0e6e4739861c08a2bc277212:b25295a8dcb74cdf98ed95dea61ef2e0@app.getsentry.com/71566')


__all__ = ['google_analytics_task']


@celery.task()
def google_analytics_task(data, user):
    """ Celery task, send Google statistics

    :param data: JSON request data from LiveChat webhook
    :type data: dict
    # :param ga: Request User ID
    # :type ga: str
    :return: ""
    """
    auth = (user.get('livechat_login'), user.get('livechat_api_key'))
    url = 'https://api.livechatinc.com/chats/'+data['chat']['id']+'/'
    headers = {"X-API-Version": "2"}
    request_data = requests.get(url, headers=headers, auth=auth)
    website = User.query.get(user.get('id')).\
        websites.filter_by(group=request_data.json()['group'][0])\
        .first_or_404()

    tags = [i.lower() for i in website.tags.split(', ')]

    for tag in request_data.json()['tags']:
        if tag.lower() in tags:
            params = urllib.parse.urlencode({
                'v': 1,
                'tid': website.google_track_id,
                'cid': data['chat']['id'],
                't': 'event',
                'ec': 'LiveChat',
                'ea': tag,
                'el': data['chat']['id']
            })
            connection = http.client.HTTPConnection(
                'www.google-analytics.com')
            connection.request('POST', '/collect', params)
    return ""