FROM ubuntu:latest
MAINTAINER Chad Peterson chapeter@cisco.com

RUN apt-get -y install \
  python \
  python-pip

COPY . /CHROnIC_Portal
WORKDIR /CHROnIC_Portal

RUN pip install -r requirements.txt

EXPOSE 5000
CMD [ "python", "./main.py" ]