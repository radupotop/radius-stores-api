import json
from operator import attrgetter, itemgetter
from pathlib import Path

from flask import Flask, abort, jsonify
from webargs import fields
from webargs.flaskparser import use_args

from model import Postcodes, db
from schema import PostcodeSchema

app = Flask(__name__)

index_args = {'postcode': fields.Str(), 'nearby': fields.Str()}


@app.route('/')
@use_args(index_args)
def index(args):
    if args.get('postcode'):
        query_result = Postcodes.select().where(
            Postcodes.postcode.contains(args['postcode'])
        )
    else:
        query_result = Postcodes.select()

    postcode_schema = PostcodeSchema(many=True)
    result = postcode_schema.dump(query_result).data
    return jsonify(result)


if __name__ == '__main__':
    db.connect()
    app.run(debug=True, port=8080)
