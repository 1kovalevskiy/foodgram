FROM python:3.8
COPY requirements.txt /
RUN pip install -r requirements.txt
WORKDIR /foodgram
COPY . /
#CMD python manage.py runserver 0.0.0.0:8000
#CMD ["gunicorn", "foodgram.wsgi:application", "--bind 0.0.0.0:8000"]
CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000
#
#FROM snakepacker/python:all as builder
#RUN python3.9 -m venv /usr/share/python3/app
#RUN /usr/share/python3/app/bin/pip install -U pip
#COPY requirements.txt /mnt/
#RUN /usr/share/python3/app/bin/pip install -Ur /mnt/requirements.txt
#
#FROM snakepacker/python:3.9 as api
#COPY --from=builder /usr/share/python3/app /usr/share/python3/app
#RUN ln -snf /usr/share/python3/app/bin/* /usr/local/bin/
#WORKDIR /mnt/
#COPY . .
#WORKDIR /mnt/foodgram/
#CMD ["/usr/share/python3/app/bin/python3", "manage.py", "runserver"]
##CMD ["/usr/share/python3/app/bin/gunicorn", "foodgram.wsgi:application", "--bind 0.0.0.0:8000"]