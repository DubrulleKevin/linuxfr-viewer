from flask import Flask
from flask_restful import Resource, Api

from linuxfr import *


app = Flask(__name__)
api = Api(app)

class LinuxFRViewer(Resource):
    def get(self):
        return get_depeches_on_page(2)

api.add_resource(LinuxFRViewer, '/')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

