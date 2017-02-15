import os
from flask import Flask, render_template, request, make_response
import config
import hashlib, hmac
from messaging import *

app = Flask(__name__)

APP_SECRET = config.APP_SECRET
SERVER_URL = config.SERVER_URL
PAGE_ACCESS_TOKEN = config.PAGE_ACCESS_TOKEN
VALIDATION_TOKEN = config.VALIDATION_TOKEN

@app.route('/')
def index():
    return render_template('index.html',message="Welcome!")

@app.route('/privacy')
def privacy():
    return render_template('privacy_policy.html')

@app.route('/webhooks', methods=['GET','POST'])
def webhooks():
    error=None
    if request.method == 'POST':
        print request.get_json()
        if is_verified(request):
            data = request.get_json()
            if data['object'] == 'page':
                return get_message(data)
        else:
            print "Unable to verify token."
            return "<(' ')>"
    else:
        if request.args['hub.mode'] == 'subscribe' and request.args['hub.verify_token'] == VALIDATION_TOKEN:
            print "Validating webhook"
            return request.args['hub.challenge']
        else:
            return 'webhooks'


@app.route('/authorize', methods=['GET'])
def authorize():
    if is_verified(request):
        data = request.get_json()
        account_linking_token = data['account_linking_token']
        redirect_uri = data['redirect_uri']
        auth_code = str(os.urandom(24))
        redirect_uri_success = redirect_uri + "&authoization_code=" + auth_code
        return render_template('authorize.html',account_linking_token=account_linking_token,redirect_uri=redirect_uri,redirect_uri_success=redirect_uri_success)
    return False


#verify signature request from Facebook.
def is_verified(req):
    if 'x-hub-signature' in req.headers:
        sig = req.headers['x-hub-signature']
        if sig is None:
            print "Couldn't validate token"
            return False
        else:
            elements = sig.split('=')
            method = elements[0]
            sig_hash = elements[1]
            expected_hash = hmac.new(config.APP_SECRET, req.data, hashlib.sha1)
            return sig_hash == expected_hash.hexdigest()
    return False

port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)
