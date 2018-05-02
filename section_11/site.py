# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import time
import hashlib
from section_11.credentials import CREDENTIALS, SECRET_KEY
from flask import Flask, render_template, request, redirect, url_for, session


# create the application object
app = Flask(__name__)
app.secret_key = SECRET_KEY  # set a key for signing cookies

# Each function is a "view" (request handler). Use decorators to route URLs to views
@app.route('/home')
def home_page():
    # render a static template
    return render_template('home.html')

@app.route('/')
def index():
    # redirects to /home
    return redirect(url_for('home_page'))


@app.route('/static')
def static_page():
    # render a static template
    return render_template('static.html')

@app.route('/dynamic')
def dynamic_page():
    # calculate server time in millis
    server_time = int(round(time.time() * 1000))

    # log raw request headers
    app.logger.debug('Request Headers: {}'.format(request.headers))

    # inject some dynamic value into a template and render it
    return render_template('dynamic.html', server_time=server_time,
                           headers=request.headers)


@app.route('/login', methods=['GET', 'POST']) # only a subset of HTTP verbs allowed here
def login_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        app.logger.info('Login attempt by {} ...'.format(username))
        if username != CREDENTIALS.get('username', None) or \
                        password != CREDENTIALS.get('password', None):
            # Auth failed
            app.logger.info('Authentication failed')
            return render_template('login.html', error='Invalid Credentials'), 401
        else:
            # Auth is successful
            app.logger.info('Authentication successful')
            # save the hashed credentials in a session data structure
            creds = (username+password).encode('utf-8')
            session['credentials'] = hashlib.md5(creds).hexdigest()
            return redirect(url_for('private_page'))
    return render_template('login.html', error=None)


@app.route('/private', methods=['GET'])
def private_page():
    # first check if we have a session: if so, then render a super-secret template
    try:
        session.pop('credentials')
        return render_template('private.html')
    except KeyError:
        return redirect(url_for('login_page'))


# start the debug server
if __name__ == '__main__':
    app.run(debug=True)