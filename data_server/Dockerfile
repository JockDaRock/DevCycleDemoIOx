FROM python:3-alpine

RUN pip install --upgrade pip setuptools wheel

RUN easy_install -U setuptools

COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 8000

COPY data_service.py .

CMD python3 data_service.py