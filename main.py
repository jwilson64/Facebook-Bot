import os
from flask import Flask, render_template, request, make_response,abort
import config
import hashlib, hmac
from messaging import *
from base64 import b64encode

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
        if is_verified(request):
            data = request.get_json()
            if data is None:
                data = json.loads(request.data)
            if data['object'] == 'page':
                return get_message(data)
        return abort(404)
    else:
        if all (k in request.args for k in ("hub.mode", "hub.verify_token")):
            if request.args['hub.mode'] == 'subscribe' and request.args['hub.verify_token'] == VALIDATION_TOKEN:
                return request.args['hub.challenge']
            else:
                return abort(404)
        else:
            return abort(404)


@app.route('/authorize', methods=['GET'])
def authorize():
    if is_verified(request):
        data = request.args
        account_linking_token = data.get('account_linking_token')
        redirect_uri = data.get('redirect_uri')
        random = os.urandom(24)
        auth_code = b64encode(random).decode("utf-8")
        redirect_uri_success = redirect_uri + "&authoization_code=" + auth_code
        return render_template('authorize.html',account_linking_token=account_linking_token,redirect_uri=redirect_uri,redirect_uri_success=redirect_uri_success)
    return abort(401)

def is_verified(req):
    if 'x-hub-signature' in req.headers:
        sig = req.headers['x-hub-signature']
        if sig is None:
            print "Couldn't validate token"
            return False
        else:
            elements = sig.split('=')
            if len(elements) < 2:
                return False
            method = elements[0]
            sig_hash = elements[1]
            data = req.data
            expected_hash = hmac.new(config.APP_SECRET, data, hashlib.sha1)
            print sig_hash
            print expected_hash.hexdigest()
            return sig_hash == expected_hash.hexdigest()
    return False

port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)
