from sender import Api
import json
import config

def get_message(data):
    for entry in data['entry']:
        page_id = entry['id']
        time_of_event = entry['time']

        for event in entry['messaging']:
            print event
            if 'optin' in event:
                received_authentication(event)
            elif 'message' in event:
                print "We have received a message"
                received_message(event)
            elif 'delivery' in event:
                received_delivery_confirmation(event)
            elif 'postback' in event:
                received_postback(event)
            elif 'read' in event:
                received_message_read(event)
            elif 'account_linking' in event:
                received_account_link(event)
            else:
                print "Unknown event has occured"

    return "Message received"

def get_response(message_text,sender_id):
    print message_text
    if message_text == 'generic':
        send_generic_message(sender_id)
    elif message_text == 'account linking':
        send_account_linking(sender_id)
    elif message_text == 'image':
        send_image_message(sender_id)
    else:
        send_text_message(sender_id, message_text)

def received_authentication(event):
    sender_id = event['sender']['id']
    recipient_id = event['recipient']['id']
    time_of_auth = event['timestamp']
    pass_through_param = event['optin']['ref']
    print "Received authentication for user %s and page %s with pass through param %s at %s" % (sender_id,recipient_id,pass_through_param,time_of_auth)
    send_text_message(sender_id, "Authentication successful!")

def received_delivery_confirmation(event):
    sender_id = event['sender']['id']
    recipient_id = event['recipient']['id']
    delivery = event['delivery']
    message_ids = delivery['mids']
    watermark = delivery['watermark']
    sequence_number = delivery['seq']

    if message_ids is not None:
        for message_id in message_ids:
            print "Received delivery confirmation for message ID: %s" % message_id

    print "Messages before %s have been delivered" % str(watermark)

def received_postback(event):
    sender_id = event['sender']['id']
    recipient_id = event['recipient']['id']
    time_of_postback = event['timestamp']
    payload = event['postback']['payload']
    send_text_message(sender_id, "Postback Called")

def received_account_link(event):
    sender_id = event['sender']['id']
    recipient_id = event['recipient']['id']
    status = event['account_linking']['status']
    auth_code = event['account_linking']['authorization_code']

    print "Received account link event for user %s with status %s and auth code %s" % (sender_id,recipient_id,auth_code)


def received_message(event):
    sender_id = event['sender']['id']
    recipient_id = event['recipient']['id']
    time_of_event = event['timestamp']
    message = event['message']
    message_text = None
    message_attachments = None
    if 'text' in message:
        message_text = message['text']
    if 'attachments' in message:
        message_attachments = message['attachments']
    if message_text is not None:
        get_response(message_text,sender_id)
    elif message_attachments:
        send_image_message(sender_id, message_attachments)

# See /me/messaging Graph API for more information on the format of the message

# When you send an image to the bot it will respond with a thumbs up
def send_image_message(recipient_id, attachments):
    message_data = {
        'recipient' : {
            'id' : recipient_id
        },
        'message' : {
            'attachment': {
                'type' : 'image',
                'payload' : {
                    'url' : 'https://scontent.xx.fbcdn.net/t39.1997-6/851557_369239266556155_759568595_n.png?_nc_ad=z-m'
                }
            }
        }
    }
    call_send_api(message_data)

# Send account linking info for authorization
def send_account_linking(recipient_id):
    message_data = {
        'recipient' : {
            'id' : recipient_id
        },
        'message': {
            'attachment' : {
                'type': 'template',
                'payload' : {
                    'template_type' : 'button',
                    'text' : 'Welcome. Link your account.',
                    'buttons' : [{
                        'type' : 'account_link',
                        'url' : config.SERVER_URL + '/authorize'
                    }]
                }
            }
        }
    }
    call_send_api(message_data)

# If all else fails send them a generic welcome message
def send_generic_message(recipient_id,message_text):
    message_data = {
        'recipient': {
            'id': recipient_id
        },
        'message': {
            'text' : "Welcome to the world of tomorrow!"
        }
    }
    call_send_api(message_data)

# By default the bot will just repeat back your previous message.
def send_text_message(recipient_id, message_text):
    message_data = {
        'recipient': {
            'id': recipient_id
        },
        'message': {
            'text': message_text
        }
    }
    call_send_api(message_data)

def call_send_api(message_data):
    api = Api()
    # Call the /me/messages graph API. access_token is your page access token. https://graph.facebook.com/me/messages?access_token=
    url = ""
    api.post(json.dumps(message_data),url)
