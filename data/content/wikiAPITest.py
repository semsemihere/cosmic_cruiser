# Python 3
# Get information about the Earth article on English Wikipedia

import requests

page = 'Earth'
url = 'https://api.wikimedia.org/core/v1/wikipedia/en/page/' + page + '/bare'


response = requests.get(url)
data = response.json()
print(data)
