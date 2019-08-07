import requests
import json
import argparse
import sys


parser = argparse.ArgumentParser()
parser.add_argument('server', help='Server')
parser.add_argument('port', type=int, help='Port')
parser.add_argument('page', type=int, help='Page number to read')
parser.add_argument('article', type=int, help='Article number to read')
args = parser.parse_args()

server = args.server
port = args.port
page = args.page
article = args.article

if page < 0:
    print('Page number must be >= 0', file=sys.stderr)
    sys.exit(1)
if article < 0:
    print('Article number must be >= 0', file=sys.stderr)
    sys.exit(2)

url = 'http://{}:{}'.format(server, port)
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

def print_news_content(news_content):
    print('================================================================================')
    print('== ' + news_content['name'] + ' ==')
    print('================================================================================\n')
    print(news_content['article'])
    for comment in news_content['comments']:
        print('================================================================================')
        print('=> Title:  ' + comment['title'])
        print('=> Author: ' + comment['author'])
        print('=> Note:   ' + comment['note'] + '\n')
        print(comment['content'] + '\n\n')


news_content = get_news_content(page, article)
print_news_content(news_content)
