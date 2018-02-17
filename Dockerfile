FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /arilot
WORKDIR /arilot
ADD . /arilot/
RUN pip install -r requirements.txt
