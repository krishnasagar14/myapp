"""
Dt. 28th Aug 2016
Description : Utility class containing methods for Tweet login, logout, timeline load etc.
Author : Krishnasagar S.
"""
import oauth2 as oauth
import cgi,requests,urllib

try:
    import json
except:
    import simplejson as json

class Tweet_Code:
    def __init__(self):
        self.consumer = oauth.Consumer('cH5nybC9i9zvzdIAsjiRm8AYt', '3uIVKYF7lNWN2E6Vl7VOjIqgt4JyRoBP97ou5KQpbdsdFcd6HN')
        self.request_token_url = 'https://api.twitter.com/oauth/request_token'
        self.access_token_url = 'https://api.twitter.com/oauth/access_token'
        self.authenticate_url = 'https://api.twitter.com/oauth/authenticate'
        self.hometimeline_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json?count=50&screen_name=%s'
        self.update_url = 'https://api.twitter.com/1.1/statuses/update.json'
    
    def TLogin(self):
        client = oauth.Client(self.consumer)
        resp, content = client.request(self.request_token_url, "GET")
        if resp['status'] != '200':
            raise Exception("Invalid response from Twitter.")
        self.request_token = dict(cgi.parse_qsl(content))
        url = "%s?oauth_token=%s" % (self.authenticate_url, self.request_token['oauth_token'])
        return url
    
    def TAuthenticate(self, request=None):
        token = oauth.Token(self.request_token['oauth_token'],self.request_token['oauth_token_secret'])
        token.set_verifier(verifier=request.GET['oauth_verifier'])
        client1 = oauth.Client(self.consumer, token)
        resp, content = client1.request(self.access_token_url, "GET")
        if resp['status'] != '200':
            print content
            raise Exception("Invalid response from Twitter.")
        self.access_token = dict(cgi.parse_qsl(content))
        return self.access_token
    
    def THome(self):
        token = oauth.Token(self.access_token['oauth_token'],self.access_token['oauth_token_secret'])
        client1 = oauth.Client(self.consumer, token)
        resp, content = client1.request(self.hometimeline_url%(self.access_token['screen_name']), "GET")
        if resp['status'] != '200':
            print content
            raise Exception("Invalid response from Twitter.")
        tweets = json.loads(content)
        return tweets
    
    def TTweet(self, s=None):
        token = oauth.Token(self.access_token['oauth_token'],self.access_token['oauth_token_secret'])
        client1 = oauth.Client(self.consumer, token)
        resp, content = client1.request(self.update_url, "POST", urllib.urlencode({'status': s}))
        if resp['status'] != '200':
            print content
            raise Exception("Invalid response from Twitter.")
        else:
            return "Success"
