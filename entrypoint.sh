#!/bin/bash
set -e

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py compilescss
echo yes | python3 manage.py collectstatic
python3 manage.py runserver 0:8080
