FROM python:3.7-alpine
WORKDIR /code
RUN python -m pip install pika --upgrade
COPY . .
CMD python app.py