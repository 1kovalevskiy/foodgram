FROM python:3.8
COPY requirements.txt /
RUN pip install -r requirements.txt
WORKDIR /foodgram
COPY . /
CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000
