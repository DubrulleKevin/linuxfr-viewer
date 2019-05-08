from flask import Flask
from flask_restful import Resource, Api

from linuxfr import *


app = Flask(__name__)
api = Api(app)

class NewsPages(Resource):
    def get(self, page_id):
        return get_news_on_page(page_id)

class News(Resource):
    def get(self, news_endpoint):
        return get_news_map(news_endpoint)

api.add_resource(NewsPages, '/news/page/<int:page_id>')
api.add_resource(News, '/news/<string:news_endpoint>')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

