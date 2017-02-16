FROM python:3-alpine

RUN apk --update add build-base libffi-dev openssl-dev

RUN pip install --upgrade pip setuptools wheel

COPY requirements.txt .

COPY static .

COPY templates .

RUN pip install -r requirements.txt

EXPOSE 80

COPY web_server.py .

CMD python3 web_server.py