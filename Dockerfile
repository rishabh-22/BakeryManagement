FROM python:3.8-slim

ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY . /code/
RUN pip3 install -r requirements.txt
EXPOSE 8000

ENTRYPOINT ["/bin/bash", "./entrypoint.sh"]