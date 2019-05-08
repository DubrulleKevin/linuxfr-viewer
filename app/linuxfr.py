import requests
from bs4 import BeautifulSoup


def get_depeches_on_page(page_number):
    url = 'https://linuxfr.org/'
    current_url = '{}?page={}/'.format(url, page_number)

    page_soup = BeautifulSoup(requests.get(current_url).text, features='html.parser')
    depeche_title_tags = [el.find('a') for el in page_soup.find_all('h1', attrs={'itemprop': u'name'})]

    depeche_titles = []
    for depeche_title_tag in depeche_title_tags:
        depeche_titles.append({'title': depeche_title_tag.string, 'url': url + depeche_title_tag['href']})

    return depeche_titles


def get_depeche_map(depeche_url):
    depeche_map = {}
    threads_list = []

    depeche_soup = BeautifulSoup(requests.get(depeche_url).text, features='html.parser')

    depeche_name = depeche_soup.find('h1', attrs={'itemprop': u'name'}).text
    depeche_map['name'] = depeche_name

    depeche_body_soup = depeche_soup.find('div', attrs={'itemprop': u'articleBody'})
    depeche_paragraphs_soup = [el.text for el in depeche_body_soup.find_all('p')]
    depeche_body = '\n\n'.join(depeche_paragraphs_soup)
    depeche_map['article'] = depeche_body

    threads_soup = depeche_soup.find('ul', attrs={'class': u'threads'})
    if threads_soup != None:
        threads_comments_soup = threads_soup.find_all('li', attrs={'class': u'comment'})
        for el in threads_comments_soup:
            title = el.find('a', attrs={'class': u'title'}).text
            author = el.find('a', attrs={'rel': u'author'}).text
            note = el.find('span', attrs={'class', u'score'}).text
            content_div = el.find('div', attrs={'class': u'content'})
            content = '\n'.join([p.text for p in content_div.find_all('p', attrs={'class': u''})])

            threads_list.append({
                'title': title,
                'author': author,
                'note': note,
                'content': content
            })

    depeche_map['threads'] = threads_list

    return depeche_map

