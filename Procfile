release: $(python manage.py migrate; python manage.py loaddata links/fixtures/users.json)
web: python manage.py runserver 0.0.0.0:$PORT
