FROM resin/raspberrypi3-alpine-python

COPY requirements.txt /requirements.txt

COPY static /static

COPY templates /templates

RUN pip install -r requirements.txt

EXPOSE 8000

COPY web_server.py /web_server.py

CMD python3 /web_server.py