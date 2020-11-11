FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7
RUN apk --update add bash nano
RUN apk update && apk add gcc && apk add musl-dev && apk add libffi-dev
COPY . /flask-app
WORKDIR /flask-app
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN ["coverage", "run", "-m", "pytest"]
RUN ["coverage", "report"]
