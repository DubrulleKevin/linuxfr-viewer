from typing import List
import requests
from bs4 import BeautifulSoup


class LinuxFRComment:
    def __init__(self, title: str, author: str, note: str, content: str) -> None:
        self._title = title
        self._author = author
        self._note = note
        self._content = content

    @property
    def title(self) -> str:
        return self._title

    @property
    def author(self) -> str:
        return self._author

    @property
    def note(self) -> str:
        return self._note

    @property
    def content(self) -> str:
        return self._content

class LinuxFRNewEntry:
    def __init__(self, title: str, url: str):
        self._title = title
        self._url = url

    @property
    def title(self) -> str:
        return self._title

    @property
    def url(self) -> str:
        return self._url

class LinuxFRNew(LinuxFRNewEntry):
    def __init__(self, title: str, url: str, content: str, comments: List[LinuxFRComment]) -> None:
        LinuxFRNewEntry.__init__(self, title, url)
        self._content = content
        self._comments = comments

    @property
    def content(self) -> str:
        return self._content

    @property
    def comments(self) -> List[LinuxFRComment]:
        return self._comments


class LinuxFRApi:
    def __init__(self):
        self._base_url = 'https://linuxfr.org'

    def get_news_on_page(self, page_number: int) -> List[LinuxFRNewEntry]:
        page_url = '{}?page={}/'.format(self._base_url, page_number)

        page_soup = BeautifulSoup(requests.get(page_url).text, features='html.parser')
        new_title_tags = [el.find('a') for el in page_soup.find_all(
            'h1',
            attrs={'itemprop': u'name'}
        )]

        news = []
        for new_title_tag in new_title_tags:
            title = new_title_tag.string
            url = self._base_url + new_title_tag['href']
            new = LinuxFRNewEntry(title, url)
            news.append(new)

        return news

    def get_new(self, new_entry: LinuxFRNewEntry) -> LinuxFRNew:
        new_soup = BeautifulSoup(requests.get(new_entry.url).text, features='html.parser')

        new_body = new_soup.find('div', attrs={'itemprop': u'articleBody'})
        new_paragraphs = [el.text for el in new_body.find_all('p')]
        new_content = '\n\n'.join(new_paragraphs)

        new_comments = []
        threads_soup = new_soup.find('ul', attrs={'class': u'threads'})
        if threads_soup is not None:
            threads_comments_soup = threads_soup.find_all('li', attrs={'class': u'comment'})
            for el in threads_comments_soup:
                title = el.find('a', attrs={'class': u'title'}).text
                author = el.find('a', attrs={'rel': u'author'}).text
                note = el.find('span', attrs={'class', u'score'}).text
                content_div = el.find('div', attrs={'class': u'content'})
                content = '\n'.join([p.text for p in content_div.find_all(
                    'p',
                    attrs={'class': u''}
                )])
                new_comments.append(LinuxFRComment(title, author, note, content))

        return LinuxFRNew(new_entry.title, new_entry.url, new_content, new_comments)
