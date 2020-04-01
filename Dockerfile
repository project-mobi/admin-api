FROM python:3.7

ADD . ../administration

WORKDIR /administration

RUN mkdir /data

COPY db.sqlite3 /data

RUN pip install -r requirements.txt

VOLUME /data

CMD ["python", "manage.py", "runserver"]
