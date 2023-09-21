# Render.com buildscript
set -o errexit

poetry install
python manage.py collectstatic --noinput
python manage.py makemigrations && python manage.py migrate
