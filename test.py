import requests
from bs4 import BeautifulSoup

def get_article():
    response = requests.get(
        url="https://en.wikipedia.org/wiki/Web_scraping",
    )
    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.find(id="firstHeading")
    print("this is the title",title.string)

get_article()
