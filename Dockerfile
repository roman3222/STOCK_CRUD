FROM python:3.11.1

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt


RUN mkdir stock
COPY . /stock
WORKDIR stock
RUN mkdir /stock/static
RUN chmod +x ./manage.py
RUN python manage.py collectstatic

EXPOSE 8000

CMD gunicorn stocks_products.wsgi:application --bind 0.0.0.0:8000
