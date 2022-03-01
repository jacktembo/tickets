FROM python:3.9-alpine
ENV PYTHONUNBUFFERED 1
# Creating working directory
RUN mkdir /code
WORKDIR /code
# Copying requirements
COPY . /code/
RUN pip install -r requirements.txt
RUN python manage.py collectstatic
RUN python manage.py makemigrations
RUN python manage.py migrate
CMD [ "gunicorn tickets.wsgi" ]