FROM python:3

WORKDIR /usr/src/app

COPY . .
RUN pip install --no-cache-dir .

EXPOSE 8000
CMD python manage.py migrate; python manage.py runserver 0.0.0.0:8000
