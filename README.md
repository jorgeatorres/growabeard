## Development

To start working on **Grow a Beard**, you need to:

1. Create a virtual environment to install all the application requirements:

        mkvirtualenv growabeard
        workon growabeard

2. Then you have to actually install those requirements:

        pip install -r requirements.txt

3. Prepare an empty database:

        sqlite3 db.sqlite3
        python manage.py migrate

4. and load the default campaign:

        python manage.py loaddata main-campaign
