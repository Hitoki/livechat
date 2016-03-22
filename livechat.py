import json

import urllib.parse
import http.client

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def base():
    return render_template('base.html')


@app.route('/livechat/ticket/', methods=['POST'])
def livechat_ticket():
    data = json.loads(request.json)
    for message in data['chat']['messages']:
        if message.get('user_type') == 'agent'\
                and '#Sell' in message.get('text'):
            params = urllib.parse.urlencode({
                'v': 1,
                'tid': 'UA-75377135-1',
                'cid': request.cookies.get('_GA'),
                't': 'event',
                'ec': 'LiveChat Category',
                'ea': 'Success Sell',
                'el': 'Sell'
            })
            connection = http.client.HTTPConnection(
                'www.google-analytics.com')
            connection.request('POST', '/collect', params)
    return ""


if __name__ == '__main__':
    # app.run(host='0.0.0.0')
    app.run()

