# Wikipedia API 
# Simply grabs wikipedia's python article & prints the first line

import wikipediaapi
wiki_wiki = wikipediaapi.Wikipedia(
    user_agent = 'MyProject', 
    language = 'en', 
    extract_format = wikipediaapi.ExtractFormat.WIKI)


# grab page sections
def print_sections(sections, level=0):
    for s in sections:
        print("%s: %s - %s" % ("*" * (level + 1), s.title, s.text[0:40]))
        print_sections(s.sections, level + 1)

# grab page in other language
def print_langlinks(page):
    langlinks = page.langlinks
    for k in sorted(langlinks.keys()):
        v = langlinks[k]
        print("%s: %s - %s: %s" % (k, v.language, v.title, v.fullurl))


def main():
    page_py = wiki_wiki.page('Python_(programming_language)')

    print("Title: ", page_py.title)
    print("First line: ", page_py.summary[0:60])
    print("Sections: ", page_py.text)

    print_sections(page_py.sections)

    print_langlinks(page_py)
    page_py_cs = page_py.langlinks['ko'] # gets wiki in korean
    print("Page - Summary: %s" % page_py_cs.summary[0:100])



if __name__ == '__main__':
    main()