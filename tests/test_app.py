#app tests
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import config
import main
import unittest
import hashlib, hmac
import json
from webhook_data import webhook_data


class BotTestCase(unittest.TestCase):

    def setUp(self):
        main.app.config['TESTING'] = True
        self.app = main.app.test_client()

    #test for making sure the webhooks work
    def test_webhooks(self):
        #start the GET challenge
        challenge = "challenged"
        rv = self.app.get("/webhooks?hub.mode=subscribe&hub.verify_token="+config.VALIDATION_TOKEN+"&hub.challenge="+challenge)
        assert rv.status == '200 OK'
        assert challenge in rv.data
        rv = self.app.get("/webhooks?hub.mode=subscribe")
        assert rv.status is not '200 OK'
        #start the POST challenge
        test_datas = webhook_data()
        for data in test_datas:
            rv = self.app.post("/webhooks",data=json.dumps(data),headers={"x-hub-signature":self.get_hash(data=json.dumps(data))})
            assert rv.status == "200 OK"
            assert rv.data == "Message received"

    #test for confirming the authorization process does work
    def test_authorization(self):
        alt = "12345" #account_linking_token
        ru = "google.com" #redirect_uri
        qs = "?account_linking_token="+alt+"&redirect_uri="+ru
        rv = self.app.get("/authorize"+qs,headers={"x-hub-signature":self.get_hash()})
        assert rv.status == '200 OK'
        assert alt in rv.data
        assert ru in rv.data
        rv = self.app.get("/authorize"+qs,headers={"x-hub-signature":"failure"})
        assert rv.status is not '200 OK'


    def get_hash(self,data=""):
        newHash = hmac.new(config.APP_SECRET, data, hashlib.sha1)
        return "POST="+newHash.hexdigest()

if __name__ == "__main__":
    print "Starting tests..."
    unittest.main()
