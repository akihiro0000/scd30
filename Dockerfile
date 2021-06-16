
FROM debian:buster

RUN apt update && apt upgrade -y
RUN apt install -y curl python3 python3-pip python3-dev python3 -V git wget vim i2c-tools

RUN pip3 install RPi.GPIO paho-mqtt datetime smbus2 scd30_i2c Flask


WORKDIR /root

RUN git clone --depth 1 https://github.com/akihiro0000/scd30.git

WORKDIR /root/scd30
