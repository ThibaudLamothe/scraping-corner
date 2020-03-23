# Structure of the repo

# The pakages used

- logzero
- selenium
- scrapy
- scrapy-splash
- And the classical `pandas` and `numpy` which need no more explanations.

# Spider Creation

# Run a spider

Into the scrapy_project app, are basically all the scrapy projects created with the `scrapy startproject project_name` command provided by the framework. The list of these project is described in a fllowing section, with brief details for each of them. And fot the biggers one, I try to maintain a Readme file directly in the project folder.

But there also are three interesting other files :

__scrapy.cfg__

When creating a new project with scrapy , it create a structure like the following : 

project_name/
project_name/
scrapy.cfg

This configuration has the structure of an `INI file` and contains two sections which are `[settings]` and `[deploy]`.

Here to have multiple projects connected by a single configuration file.


__run_spider.py__

__spider_dispatch.json__

# Use of Docker

# Project list

> Amazon  : OK
  - Spider works
  - Full project : Hackathon for XHEC students 2020
  - Needs further processing
  - Tried to scrap with Splash (useful lines still in spider and settings code)

> Booking
  - Spider does not work

> Carrefour
  - Uses Splash
  - Working
  - Code to imprve
  
> LBC : leboncoin
  - Spider is working 80%
  - Trying to repare buttemporary banned from LBC 
  - UnitTesting in process (To be finished when ban is over or after using proxies)


> PV : ParuVendu
  - Works Fine
  - Logging not updated
  - Code to clean
  - No Unit Testing (not in a hurry as the structure as not changed in more than one year)
  
> SL : SeLoger
  - Does not work : seems to be a lot of things to improve

> TA : TripAdvisor
  - Multilple spiders
    - airlines : not working
    - hotels : not working
    - restaurant (information about restos) : working but quality to be imporved
    - restaurant (reviews of restos) : working but stops after few iterations (only 30k reviews for Paris => understand why)

> TrustPilot
  - Parts are working but I don't know how


# Using scraping app

