# Wikipedia API 
# Simply grabs wikipedia's python article & prints the first line

import wikipediaapi
wiki_wiki = wikipediaapi.Wikipedia('MyProject', 'en')

page_py = wiki_wiki.page('Python_(programming_language)')

print(page_py.title)
print(page_py.summary[0:60])