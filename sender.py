import urllib2


# Made an api class in case more integration is needed in the future.
# This will be far more useful as the bot is built out.

class Api:

    def post(self,data,url,headers={'Content-type': 'application/json'}):
        request = urllib2.Request(url,data,headers)
        try:
            response = urllib2.urlopen(request)
            print response
        except urllib2.HTTPError as e:
            print "Fatal error log info: " + url
            print data
            print e
