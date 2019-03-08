import json
from pathlib import Path

import requests


def build():
    """
    Build postcodes json file.
    """
    stores_file = Path('./stores.json')
    stores = json.loads(stores_file.read_bytes())

    postcodes = [s['postcode'] for s in stores]

    resp = requests.post(
        'https://api.postcodes.io/postcodes', json={'postcodes': postcodes}
    )
    Path('./postcodes.json').write_bytes(resp.content)


build()
