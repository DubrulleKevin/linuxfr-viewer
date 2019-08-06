import requests
import json
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("server", help="Server")
parser.add_argument("port", type=int, help="Port")
parser.add_argument("page", type=int, help="Page number to read")
parser.add_argument("article", type=int, help="Article number to read")
args = parser.parse_args()

server = args.server
port = args.port
page = args.page
article = args.article

url = 'http://{}:{}'.format(server, port)
news_pages_endpoint = url + '/news/page/{}'


def get_news_on_page(page_number):
    return json.loads(requests.get(news_pages_endpoint.format(page_number)).text)

def get_news_content(news_endpoint):
    return json.loads(requests.get(url + news_endpoint).text)


news_url = get_news_on_page(page)[article]['url']
news_content = get_news_content(news_url)

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

