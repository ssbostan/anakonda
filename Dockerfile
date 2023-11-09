FROM python:3.11-alpine


LABEL maintainer="Saeid Bostandoust <ssbostan@yahoo.com>"

ENV ANAKONDA_API_ENV=production
ENV ANAKONDA_API_DEBUG=0
ENV ANAKONDA_API_SECRET_KEY=secretkey
ENV ANAKONDA_API_JSON_PRETTYPRINT=0
ENV ANAKONDA_API_DATABASE_URI=None
ENV ANAKONDA_API_TIMEZONE=Europe/London

EXPOSE 8080

WORKDIR /opt/app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN adduser -DH -g anakonda anakonda

USER 1000

ENTRYPOINT ["gunicorn"]

CMD ["-c", "gunicorn.conf.py"]
