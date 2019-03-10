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
    elif args.get('nearby'):
        result = Postcodes.select().where(Postcodes.postcode == args['nearby'])
        lat = round(result[0].latitude, 2)
        lng = round(result[0].longitude, 2)
        print(lat, lng)
    else:
        query_result = Postcodes.select().order_by(Postcodes.name)

    postcode_schema = PostcodeSchema(many=True)
    result = postcode_schema.dump(query_result).data
    return jsonify(result)


if __name__ == '__main__':
    db.connect()
    app.run(debug=True, port=8080)
