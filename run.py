import json
from operator import attrgetter, itemgetter
from pathlib import Path

from flask import Flask, abort, jsonify
from scipy import spatial
from webargs import fields
from webargs.flaskparser import use_args

from model import Postcodes, db
from schema import PostcodeSchema

app = Flask(__name__)

index_args = {
    'postcode': fields.Str(),
    'nearby': fields.Str(),
    'radius': fields.Float(missing=0.25),
}


@app.route('/')
@use_args(index_args)
def index(args):
    """
    The main route of the app.
    Supports:

    - partial postcode lookup using the postcode query parameter: ?postcode=SW11
    - exact postcode matching and neighbour lookup using the combined
      nearby and radius query parameters: ?nearby=NW1+9EX&radius=0.1

    Uses KDTree from scipy to lookup neighbouring coordinates.
    """
    if args.get('postcode'):
        query_result = Postcodes.select().where(
            Postcodes.postcode.contains(args['postcode'])
        )
    elif args.get('nearby') and args.get('radius'):
        all_coordinates = Postcodes.select().where(
            Postcodes.longitude, Postcodes.latitude
        )
        _result = Postcodes.select().where(Postcodes.postcode == args['nearby'])
        if _result:
            target = _result[0]
        else:
            # Can be 400 or 404, this is up for debate.
            abort(400)

        coordinates_idx = tuple((c.longitude, c.latitude) for c in all_coordinates)
        tree = spatial.KDTree(coordinates_idx)
        nearby_idx = tree.query_ball_point(
            (target.longitude, target.latitude), args['radius']
        )

        query_result = []
        for idx in nearby_idx:
            query_result.append(all_coordinates[idx])
        query_result.sort(key=attrgetter('latitude'), reverse=True)

    else:
        query_result = Postcodes.select().order_by(Postcodes.name)

    postcode_schema = PostcodeSchema(many=True)

    if args.get('radius') == 0.25:
        del args['radius']

    result = {'query': args, 'results': postcode_schema.dump(query_result).data}

    return jsonify(result)


if __name__ == '__main__':
    db.connect()
    app.run(debug=True, port=8080)
