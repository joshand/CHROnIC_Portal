FROM chapeter/chronic_docker
MAINTAINER Chad Peterson chapeter@cisco.com


COPY . /CHROnIC_Portal
WORKDIR /CHROnIC_Portal

RUN pip install -r requirements.txt


EXPOSE 5000
CMD [ "python", "./main.py" ]
