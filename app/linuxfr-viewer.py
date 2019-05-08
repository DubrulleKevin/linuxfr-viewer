import requests
from bs4 import BeautifulSoup
import sys


base_url = 'https://linuxfr.org/'

def _get_depeche(url, page_number = 1):
    current_url = '{}?page={}/'.format(url, page_number)

    page_soup = BeautifulSoup(requests.get(current_url).text, features='html.parser')
    depeche_title_tags = [el.find('a') for el in page_soup.find_all('h1', attrs={'itemprop': u'name'})]

    depeche_titles = []
    for depeche_title_tag in depeche_title_tags:
        depeche_titles.append({'title': depeche_title_tag.string, 'url': depeche_title_tag['href']})

    i = 0
    for depeche_title in depeche_titles:
        print('{}: {}'.format(i, depeche_title['title']))
        i = i + 1

    print('\n{}: Next page\n'.format(i))

    choice = -1
    while choice < 0 or choice > len(depeche_titles):
        try:
            choice = int(input('Choice: '))
        except ValueError:
            print('Error: please input a number...', file=sys.stderr)
        except KeyboardInterrupt:
            sys.exit(1)

    if choice == i:
        return _get_depeche(url, page_number + 1)

    return BeautifulSoup(requests.get(url + depeche_titles[choice]['url']).text, features='html.parser')

depeche_soup = _get_depeche(base_url)

article_body = depeche_soup.find('div', attrs={'itemprop': u'articleBody'})
articles_paragraphs = [el.text for el in article_body.find_all('p')]
article = '\n\n'.join(articles_paragraphs)

print(article)

threads_soup = depeche_soup.find('ul', attrs={'class': u'threads'})
if threads_soup == None:
    sys.exit(0)
threads_comments_soup = threads_soup.find_all('li', attrs={'class': u'comment'})
for el in threads_comments_soup:
    title = el.find('a', attrs={'class': u'title'}).text
    author = el.find('a', attrs={'rel': u'author'}).text
    note = el.find('span', attrs={'class', u'score'}).text
    content_div = el.find('div', attrs={'class': u'content'})
    content = '\n'.join([p.text for p in content_div.find_all('p', attrs={'class': u''})])
    print('=> Posted by: ' + author)
    print('   Title:     ' + title)
    print('   Note:      ' + note + '\n')
    print(content + '\n\n')

