#Data for testing the webhooks

#data for testing a text style message
def text_data():
    return {
        "object": "page",
        "entry" : [{
            "id" : "tester",
            "time": "12:46PM",
            "messaging" : [{
                "timestamp" : "Today",
                "sender": {
                    "id": "tester"
                },
                "recipient":{
                    "id": "tester"
                },
                'message' : {
                    "text": "This is a test"
                }
            }]
        }]
    }
#Test that an image can be sent
def image_data():
    return {
        "object": "page",
        "entry" : [{
            "id" : "tester",
            "time": "12:46PM",
            "messaging" : [{
                "timestamp" : "Today",
                "sender": {
                    "id": "tester"
                },
                "recipient":{
                    "id": "tester"
                },
                'message' : {
                    'attachment': {
                        'type' : 'image',
                        'payload' : {
                            'url' : 'https://scontent.xx.fbcdn.net/t39.1997-6/851557_369239266556155_759568595_n.png?_nc_ad=z-m'
                        }
                    }
                }
            }]
        }]
    }

#add webhook test dat a to this array
def webhook_data():
    return [text_data(),image_data()]
