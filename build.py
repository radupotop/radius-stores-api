import json
from pathlib import Path
import requests


from model import db, Postcodes


def build():
    db.connect()
    db.create_tables((Postcodes,))

    stores_file = json.loads(Path('./stores.json').read_bytes())
    postcodes_file = json.loads(Path('./postcodes.json').read_bytes())['result']

    print('Number of stores: ', len(stores_file))

    with db.atomic():
        for idx, store in enumerate(stores_file):
            print('Store:', store['name'], store['postcode'])

            if postcodes_file[idx].get('result'):
                Postcodes.create(
                    name=store['name'],
                    postcode=store['postcode'],
                    latitude=postcodes_file[idx]['result']['latitude'],
                    longitude=postcodes_file[idx]['result']['longitude'],
                )
            else:
                Postcodes.create(name=store['name'], postcode=store['postcode'])


def fetch_postcodes():
    """
    Fetch data for postcodes and cache to json file.
    This only needs to run once.
    """
    stores_file = Path('./stores.json')
    stores = json.loads(stores_file.read_bytes())

    postcodes = [s['postcode'] for s in stores]

    resp = requests.post(
        'https://api.postcodes.io/postcodes', json={'postcodes': postcodes}
    )
    Path('./postcodes.json').write_bytes(resp.content)


build()
