# -*- coding: utf-8 -*-
import time
from twython import Twython
from urllib.parse import quote

CONSUMER_KEY = '56RUCZl3CoC6J8xG6Wzfuc7vD'
CONSUMER_SECRET = 'rurZLUGbTjaTAfJ7p2TPKypidUHI4zzvzhZdczBXDHAOq5XAHX'
OAUTH_TOKEN = '66928398-GdrNYVBnlBqHHEQ3mD1bfTnLobBWQzJFxc5BI70Ev'
OAUTH_TOKEN_SECRET = 'QFwNNyOK6Ow0HHF0cAs3aZKZ1jrPJvZGF7L6HdXVZAald'


twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
query = quote('maluma descarga directa')
results = twitter.search(q='"maluma descarga directa"', count=100)
i = 0
print(results)
tweets = results['statuses']
for t in tweets[0:100]:
    print(t['text'])
#         try:
#             url = str(result['entities']['urls'][0]['url'])
#         except:
#             url = ''
#         try:
#             Hash = str(result['entities']['hashtags'][0]['text'])
#         except:
#             Hash = ''
#         print('------------------------------------------------------------------------')
#         print ('fecha:' + result['created_at'])
#         print ('usuario:' + result['user']['screen_name'])
#         print ('texto:' + result['text'])
#         print ('hashtags:' + Hash)
#         print ('infringing:' + url)
#         print('------------------------------------------------------------------------')
#         if i == 10:
#             i = 0
#             time.sleep(3)
# else:
#     print('No encontró nada.')