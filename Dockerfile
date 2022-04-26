FROM python:3.10.0rc1-buster

RUN mkdir /code
WORKDIR /code

COPY . .
RUN pip install --upgrade pip  && pip install -r requirements.txt

CMD ["gunicorn forecast.wsgi"]
