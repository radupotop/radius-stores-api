import json
from pathlib import Path
from operator import attrgetter, itemgetter

from flask import Flask, abort, jsonify
from webargs import fields
from webargs.flaskparser import use_args

app = Flask(__name__)

index_args = {'postcode': fields.Str(), 'radius': fields.Str()}

stores_file = Path('./stores.json')
stores = json.loads(stores_file.read_bytes())
stores.sort(key=itemgetter('name'))


@app.route('/')
@use_args(index_args)
def index(args):
    try:
        return jsonify(*filter(lambda s: args['postcode'] in s['postcode'], stores))
    except KeyError:
        return jsonify(stores)


if __name__ == '__main__':
    app.run(debug=True, port=8080)
