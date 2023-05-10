FROM python:3.11.1


RUN mkdir stock
WORKDIR stock

ADD . /stock/
ADD .env.docker /stock/.env

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]
