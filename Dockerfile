FROM python:3

ENV LANG C.UTF-8

COPY requirements.txt /

RUN apt update -y && \
    apt install python3 -y && \
    apt install jq -y && \
    python3 -m ensurepip && \
    rm -r /usr/local/lib/python*/ensurepip && \
    python3 -m pip install -r requirements.txt

COPY monitor.py /
COPY run.sh /
COPY config.py /

RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
