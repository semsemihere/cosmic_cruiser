import json
import requests

language_code = 'en'
search_query = 'web scraping'
number_of_results = 1
headers = {
  # 'Authorization': 'Bearer YOUR_ACCESS_TOKEN',
  'User-Agent': 'YOUR_APP_NAME (YOUR_EMAIL_OR_CONTACT_PAGE)'
}

base_url = 'https://api.wikimedia.org/core/v1/wikipedia/'
endpoint = '/search/page'
url = base_url + language_code + endpoint
parameters = {'q': search_query, 'limit': number_of_results}
response = requests.get(url, params=parameters)
response = json.loads(response.text)

for page in response['pages']:
  display_title = page['title']
  print(display_title)
  article_url = 'https://' + language_code + '.wikipedia.org/wiki/' + page['key']
  try:
    article_description = page['description']
  except:
    article_description = 'a Wikipedia article'
  try:
    thumbnail_url = 'https:' + page['thumbnail']['url']
  except:
    thumbnail_url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/200px-Wikipedia-logo-v2.svg.png'