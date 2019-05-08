import requests
import json


url = 'http://localhost:5000'
news_pages_endpoint = url + '/news/page/{}'


def get_news_on_page(page_number):
    return json.loads(requests.get(news_pages_endpoint.format(page_number)).text)

def get_news_content(news_endpoint):
    return json.loads(requests.get(url + news_endpoint).text)



news_0_url = get_news_on_page(1)[0]['url']
news_0_content = get_news_content(news_0_url)

print('================================================================================')
print('== ' + news_0_content['name'] + ' ==')
print('================================================================================\n')
print(news_0_content['article'])
for comment in news_0_content['comments']:
    print('================================================================================')
    print('=> Title:  ' + comment['title'])
    print('=> Author: ' + comment['author'])
    print('=> Note:   ' + comment['note'] + '\n')
    print(comment['content'] + '\n\n')

