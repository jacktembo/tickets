FROM tickets
WORKDIR /app
COPY . /app
RUN python manage.py makemigrations
RUN python manage.py migrate
CMD gunicorn tickets.wsgi
