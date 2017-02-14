FROM resin/rpi-raspbian

RUN apt-get update
RUN apt-get install mongodb-server
RUN mkdir /data
RUN mkdir /data/db
EXPOSE 27017 28017

CMD ["mongod" ]