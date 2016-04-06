import requests
import urllib.parse
import http.client

from celery import Celery

from livechat import app

celery = Celery(app.name)

celery.conf.update(app.config)

__all__ = ['google_analytics_task']


@celery.task()
def google_analytics_task(data, ga, user):
    """ Celery task, send Google statistics

    :param data: JSON request data from LiveChat webhook
    :type data: dict
    :param ga: Request cookie User ID
    :type ga: str
    :return: ""
    """
    auth = (user.livechat_login, user.livechat_api_key)
    url = 'https://api.livechatinc.com/chats/'+data['chat']['id']+'/'
    headers = {"X-API-Version": "2"}
    request_data = requests.get(url, headers=headers, auth=auth)

    for tag in request_data.json()['tags']:
        params = urllib.parse.urlencode({
            'v': 1,
            'tid': user.google_track_id,
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