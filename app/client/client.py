import api
import argparse

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

def main_cli():
    print_news_content(api.get_news_content(0, 0))

def main_tk():
    import clienttk
    client_tk = clienttk.ClientTk()
    client_tk.mainloop()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--cli', help='CLI interface', action='store_true')
    args = parser.parse_args()

    if args.cli:
        main_cli()
    else:
        main_tk()
