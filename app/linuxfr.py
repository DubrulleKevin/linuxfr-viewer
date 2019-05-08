import requests
from bs4 import BeautifulSoup


_linuxfr_url = 'https://linuxfr.org/'


def get_news_on_page(page_number):
    current_url = '{}?page={}/'.format(_linuxfr_url, page_number)

    page_soup = BeautifulSoup(requests.get(current_url).text, features='html.parser')
    news_title_tags = [el.find('a') for el in page_soup.find_all('h1', attrs={'itemprop': u'name'})]

    news_titles = []
    for news_title_tag in news_title_tags:
        news_titles.append({'title': news_title_tag.string, 'url': _linuxfr_url + news_title_tag['href']})

    return news_titles


def get_news_map(news_endpoint):
    news_url = _linuxfr_url + '/news/' + news_endpoint

    news_map = {}
    threads_list = []

    news_soup = BeautifulSoup(requests.get(news_url).text, features='html.parser')

    news_name = news_soup.find('h1', attrs={'itemprop': u'name'}).text
    news_map['name'] = news_name

    news_body_soup = news_soup.find('div', attrs={'itemprop': u'articleBody'})
    news_paragraphs_soup = [el.text for el in news_body_soup.find_all('p')]
    news_body = '\n\n'.join(news_paragraphs_soup)
    news_map['article'] = news_body

    threads_soup = news_soup.find('ul', attrs={'class': u'threads'})
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

    news_map['comments'] = threads_list

    return news_map

