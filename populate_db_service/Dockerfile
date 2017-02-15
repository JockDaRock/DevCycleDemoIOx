FROM python:3-alpine

RUN apk --update add build-base libffi-dev openssl-dev

RUN pip install --upgrade pip setuptools wheel

COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 8000

COPY mongo_db_service.py .

CMD python mongo_db_service.py