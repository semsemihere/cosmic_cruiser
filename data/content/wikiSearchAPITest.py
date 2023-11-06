# Python 3
# Get the HTML version of the Earth article on English Wikipedia

import requests
page = input("What would you like to search: ")
url = 'https://api.wikimedia.org/core/v1/wikipedia/en/page/' + page + '/html'


response = requests.get(url)
print(response.text)
