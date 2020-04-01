FROM python:3.7

ADD . ../administration

WORKDIR /administration

RUN pip install -r requirements.txt

CMD ["python", "manage.py", "runserver"]
