import json
import threading

import urllib.parse
import http.client

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def base():
    return render_template('base.html')


@app.route('/livechat/ticket/', methods=['POST'])
def livechat_ticket():
    """ Send new track to Google analytic from LiveChatInc webhooks.
    (If "sales" is in chat tags)
    :return: ""
    """
    data = request.json
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


if __name__ == '__main__':
    app.run(host='0.0.0.0')

