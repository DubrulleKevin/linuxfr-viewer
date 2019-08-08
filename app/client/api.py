import requests
import json
import sys

url = 'http://{}:{}'.format('192.168.1.200', 5000)
news_pages_endpoint = url + '/news/page/{}'

def get_news_on_page(page_number):
    return json.loads(requests.get(news_pages_endpoint.format(page_number)).text)

def get_news_url(news_page, news_number):
    try:
        return get_news_on_page(news_page)[news_number]['url']
    except IndexError:
        print('Article not found', file=sys.stderr)
        sys.exit(3)

def get_news_content(news_page, news_number):
    return json.loads(requests.get(url + get_news_url(news_page, news_number)).text)


#class LinuxFrApi:
    #self __init__(self, server='localhost', port=5000):

