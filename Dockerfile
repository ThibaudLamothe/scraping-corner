FROM python:3.7.2

RUN mkdir /scraping-corner
RUN mkdir /scraping-corner/scrapy_project
RUN mkdir /scraping-corner/scrapped_data
RUN mkdir /scraping-corner/scripts
RUN mkdir /scraping-corner/spider_testing

COPY requirements.txt /scraping-corner/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r /scraping-corner/requirements.txt

RUN apt update
RUN apt install nano

EXPOSE 8050
EXPOSE 8051
EXPOSE 8888
EXPOSE 8889