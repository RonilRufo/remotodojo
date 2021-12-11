#! /bin/bash
# install dev dependencies that weren't included in image
poetry install --no-interaction

python /remotodojo/manage.py collectstatic --noinput
python /remotodojo/manage.py migrate --noinput
python /remotodojo/manage.py runserver 0.0.0.0:8000
