import requests

from flask import render_template, request, flash, url_for, redirect
from flask.ext.login import login_user, logout_user, login_required,\
    _get_user

from werkzeug.datastructures import ImmutableMultiDict

from livechat import app, db
from livechat.models import User, Website
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
            flash('Logged in successfully by {}.'.format(user.username))
            return redirect(url_for('index'))
    return render_template('login.html', error=errors, form=form)


@app.route('/logout')
@login_required
def logout():
    """
    Logout endpoint

    :return: redirect(url_for('index'))
    """
    logout_user()
    flash('You were logged out.')
    return redirect(url_for('index'))


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    """
    Update profile endpoint

    :return: POST "redirect(url_for('index'))"
    :return: GET "render_template('update_profile.html')"
    """

    user = _get_user()
    if request.method == 'POST':
        user.update_user_data(request.form)
        flash('Profile updated successfully')
        return redirect(url_for('index'))
    else:
        request.form = ImmutableMultiDict([
            ('livechat_login', user.livechat_login or ''),
            ('livechat_api_key', user.livechat_api_key or '')
        ])
        return render_template('update_profile.html', error={})


@app.route('/<user_hash>/', methods=['GET', 'POST'])
def livechat_ticket(user_hash):
    """

    Send new track to Google analytic from LiveChatInc webhooks endpoint.
    :return: POST ""
    :return: GET "render_template('chat_page.html', **ctx)"
    """
    user = User.query.filter_by(hash=user_hash).first_or_404()
    # google_analytics_task.apply_async(
    # args=({"chat": {"id": "O5B9JQE8ZU"}}, user.serialize()),
    # countdown=6)
    if request.get_json():
        app.logger.error('Webhook: {}'.format(request.get_json()))
        google_analytics_task.apply_async(args=(request.get_json(), user.serialize()), countdown=6)
        return ""
    if user.websites.first():
        ctx = {
            'google_track_id': user.websites.first().google_track_id
        }
    else:
        ctx = {
            'google_track_id': 'No current websites'
        }
    return render_template('chat_page.html', **ctx)


@app.route('/help_install/')
@login_required
def help_install():
    """
    Help page for install LiveChat

    :return: render_template('help_page.html')
    """
    print(dir(request))
    return render_template('help_page.html')


@app.route('/websites/create', methods=['GET', 'POST'])
@login_required
def create_website():
    """
    Create website endpoint

    :return: POST "redirect(url_for('index'))"
    :return: GET "render_template('create_website.html')"
    """
    user = _get_user()

    if request.method == 'POST':
        data = {}
        for key, value in dict(request.form).items():
            data[key] = value[0]
        website = Website(**data)
        website.user_id = user.id
        db.session.add(website)
        db.session.commit()
        flash('Website created successfully')
        return redirect(url_for('index'))
    else:
        auth = (user.livechat_login, user.livechat_api_key)
        url = 'https://api.livechatinc.com/groups/'
        headers = {"X-API-Version": "2"}
        request_data = requests.get(url, headers=headers, auth=auth).json()
        return render_template(
            'create_website.html', error={}, groups=request_data)


@app.route('/websites/<web_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_website(web_id):
    """
    Edit website endpoint

    :return: POST "redirect(url_for('index'))"
    :return: GET "render_template('edit_website.html')"
    """
    user = _get_user()
    website = Website.query.get_or_404(web_id)

    if request.method == 'POST':
        data = {}
        for key, value in dict(request.form).items():
            data[key] = value[0]
        Website.query.filter_by(id=web_id).update(data)
        db.session.commit()
        flash('Website {} updated successfully'.format(website.title))
        return redirect(url_for('index'))
    else:
        auth = (user.livechat_login, user.livechat_api_key)
        url = 'https://api.livechatinc.com/groups/'
        headers = {"X-API-Version": "2"}
        request_data = requests.get(url, headers=headers, auth=auth).json()
        return render_template(
            'edit_website.html', error={},
            groups=request_data, website=website)


@app.route('/websites/<web_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_website(web_id):
    """
    Delete website endpoint

    :return: POST "redirect(url_for('index'))"
    :return: GET "render_template('delete_website.html')"
    """
    website = Website.query.get_or_404(web_id)
    if request.method == 'POST':
        db.session.delete(website)
        db.session.commit()
        flash('Website deleted successfully')
        return redirect(url_for('index'))
    else:
        return render_template(
            'delete_website.html', error={}, website=website)
