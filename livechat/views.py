from flask import render_template, request, flash, url_for, redirect
from flask.ext.login import login_user, logout_user, login_required

from livechat import app
from livechat.models import User
from livechat.tasks import google_analytics_task


__all__ = ['index', 'livechat_ticket']


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Index endpoint

    :return: render_template: index.html
    """
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login endpoint

    :return: render_template('login.html') with errors
    """
    errors = {}
    form = request.form
    if request.method == 'POST':
        user = User.query.filter_by(
            username=request.form.get('username')).first()
        if user is None:
            errors.update({'username': 'Unknown Username'})
        elif not user.check_password(request.form.get('password')):
            errors.update({'password': 'Invalid password'})
        if not errors:
            login_user(user)
            user.update_user_data(request.form)
            flash('Logged in successfully by {}.'.format(user.username))
            return redirect(url_for('help_install'))
    return render_template('login.html', error=errors, form=form)


@app.route('/logout')
def logout():
    """
    Logout endpoint

    :return: redirect(url_for('index'))
    """
    logout_user()
    flash('You were logged out.')
    return redirect(url_for('index'))


@app.route('/<user_hash>/', methods=['GET', 'POST'])
def livechat_ticket(user_hash):
    """

    Send new track to Google analytic from LiveChatInc webhooks endpoint.
    :return: POST ""
    :return: GET "render_template('chat_page.html', **ctx)"
    """
    user = User.query.filter_by(hash=user_hash).first_or_404()
    if request.get_json():
        # For develop task

        google_analytics_task(
            request.get_json(), request.get_json()['chat']['id'], user)
        # google_analytics_task(
        #     request.get_json(), request.cookies.get('_GA'), user)

        # Celery task
        # google_analytics_task.apply_async(
        #     args=(request.get_json(), request.cookies.get('_GA')),
        #     countdown=600)
        return ""
    ctx = {
        'google_track_id': user.google_track_id
    }
    return render_template('chat_page.html', **ctx)


@app.route('/help_install/')
@login_required
def help_install():
    """
    Help page for install LiveChat

    :return: redirect(url_for('help_install'))
    """
    return render_template('help_page.html')

