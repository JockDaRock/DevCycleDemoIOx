FROM resin/raspberrypi3-alpine-python

COPY requirements.txt /requirements.txt

RUN pip3 install -r /requirements.txt

EXPOSE 8000

COPY data_collection.py /data_collection.py

CMD python3 /data_collection.py