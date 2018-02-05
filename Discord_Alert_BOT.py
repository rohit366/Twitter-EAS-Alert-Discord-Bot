'''
MIT License

Copyright (c) 2018 Vincent Maggard

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

from twitter import *
import json
import requests
import re
import configparser
from pathlib import Path

filename = Path("BOT_Config.cfg")
if filename.is_file():
   print("File Found!")
   config = configparser.RawConfigParser()
   config.read('BOT_Config.cfg')
else:
   print("Config File 'BOT_Config.cfg' Not Found!")
   exit()


if config.get('main', 'discord_webhook'):
   discord_webhook = config.get('main', 'discord_webhook')
else:
   discord_webhook = None

if discord_webhook == None:
   print("Discord Webhook Not Entered Or Invaild!")
   exit()

###########################################
# DISCORD                                 #
###########################################
def msg_send(message):
    data = {
        'content' : message
    }

    json_str = json.dumps(data)
    #print(json_str)
    headers = {'content-type' : 'application/json'}
    r = requests.post('WEBHOOK HERE', data = json_str, headers=headers)
    


###########################################
# TWITTER                                 #
###########################################
if config.get('main', 'consumer_key'):
   consumer_key = config.get('main', 'consumer_key')
else:
   consumer_key = None
if config.get('main', 'consumer_secret'):
   consumer_secret = config.get('main', 'consumer_secret')
else:
   consumer_secret = None
if config.get('main', 'access_token'):
   access_token = config.get('main', 'access_token')
else:
   access_token = None
if config.get('main', 'access_token_secret'):
   access_token_secret = config.get('main', 'access_token_secret')
else:
   access_token_secret = None

if consumer_key == None or consumer_secret == None or access_token == None or access_token_secret == None:
   print("Twitter Data Invaid Or Not Entered!")
   exit()

config = {}


auth = OAuth(access_token, access_token_secret, consumer_key, consumer_secret)
stream = TwitterStream(auth = auth, secure = True)
tweet_iter = stream.statuses.filter(follow= '2686948915' , replies='None')
for tweet in tweet_iter:
    #print(tweet)
    try:
        message_txt = str(tweet["text"])
        retweets = re.search("(@EASAlerts)", message_txt)
        if retweets != None:
           continue
        msg_send(message_txt)
    except Exception:
        continue

