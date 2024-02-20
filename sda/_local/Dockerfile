FROM python:3.8.18

COPY ./sda/requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

WORKDIR /sda/

COPY ./sda/ .

EXPOSE 8050

ENTRYPOINT "/sda/_local/entrypoint.sh"
