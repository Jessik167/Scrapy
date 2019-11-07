import requests
#https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
url = 'http://iflowmusic.com'

response = requests.get(url)
print(response.status_code) # 404
#print(response.text) # Prints the raw HTML