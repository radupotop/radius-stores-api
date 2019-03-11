The `postcodes.db` file is included with the source code for simplicity.

But you might need to remove and recreate this file for the app to work
on your machine.

All the commands are run within `venv`.

## Initial building

    rm postcodes.db
    python build.py

## Running

    python run.py

## The app supports

- partial postcode lookup using the postcode query parameter: `?postcode=SW11`
- exact postcode matching and neighbour lookup using the combined
    nearby and radius query parameters: `?nearby=NW1+9EX&radius=0.1`

## Examples

Lookup:

- http://127.0.0.1:8080/?postcode=NW1
- http://127.0.0.1:8080/?postcode=GU

Radius:

- http://127.0.0.1:8080/?nearby=CR0+4NX&radius=0.15
- http://127.0.0.1:8080/?nearby=NW1+9EX&radius=0.1


## Libraries used

- Flask for the API
- Marshmallow for the schema
- Peewee for the model
- Sqlite database
- KDTree from Scipy to lookup neighbouring coordinates
