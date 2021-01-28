# Introduction

The scraping corner is a repository where I keep track of all my scraping projects in a single place. Since I've been working on a bunch of them, I found that it was the most practical way to operate.
Then anytime I need to use scraping in a project I develop the scraping part in here and use it as a third pary API from the main project.

In this README file, I'll introduce the structure and the way I work with this repo and keep a list of the website.

> Disclaimer : websites are alive objects and evolve, which means that a scraping process workint at a specific date, might encounter difficulties the following day due to source's website structural change. The spiders available in this repo have been designed for specific uses and are not maintained if not necessary. That's why I'm also working on Testing Spider, to detect easily which selectors should be modified to correct an old spider.
# Structure of the repo
```
├── .gitignore                   <-  contains description of files not to upload on git repository  
├── README.md                    <-  the top-level README : repo description  
├── docker-compose.yml           <-  running scraping env through docker and docker-compose  
├── Dockerfile                   <-  running scraping env through docker and docker-compose  
├── requirements.txt             <-  contains necessary packages (incorporated in  Dockerfile)  
├── notebook                     <== To prepare a scraping I use to prepare the css selectors through notebooks 
    ├── *.ipynb                  <-  usually with one notebook per spider or per website
    ├── *.ipynb                  <-  usually with one notebook per spider or per website
    ├── ...
├── scrapy_project               <== contains all scripts relative to scrapy
    ├── scrapy.cfg               <-  default scrapy file. Used to deal with multiple projects.
    ├── run_spider.py            <-  start the scraping process
    ├── spider_dispatch.json     <-  configurates the scraping process
    ├── ProjectWebsite1          <== folder created by scrapy for a first project (see "Using scrapy" for more explanations)
    ├── ProjectWebsite2          <== folder created by scrapy for a first project (see "Using scrapy" for more explanations)
    ├── ...
├── scripts                      <== contains specific for common tasks while scraping
    ├── count_line.py            <-  used to count the number of released item from an executing scraping
    ├── display_info.py          <-  used to display information about the released items from an executing scraping
    ├── jl_to_df.py              <-  converts a json line file into a pandas DataFrame 
├── selenium                     <== contains all scripts relative to scrapy
    ├── selenium_basics.py       <-  selenium basics actions wrapped into a Python Class to simplify exploration process
    ├── chromedriver             <-  not uploaded, but this its position.
├── template                     <== template files
    ├── ...                      <- (TBD)
├── tor                          <== experimentation to crawl the darkweb
  ``` 


# Using Scrapy

- The main tool I use to perform web scraping is `Scrapy` ([documentation](https://docs.scrapy.org/en/latest/))


- Into the `scrapy_project` folder, are all the scrapy projects created with the `scrapy startproject project_name` provided by the framework.
- The list of these project is described in a following section, with brief details and status for each of them.
- For the bigger scraping projects, I try to maintain a README file directly into the project folder.

## Default Scrapy files

When launching a new project with scrapy, it automatically creates the following structure : 

```
├── project_name/
  ├── scrapy.cfg
  ├── project_name/
    ├── spiders 
    ├── items.py
    ├── middlewares.py
    ├── pipelines.py
    ├── settings.py
```

__scrapy.cfg__

- This configuration file has the structure of an `INI file` and contains two sections which are `[settings]` and `[deploy]`. It is also used to manage multiple projects.
- It is necessary to have it at the root folder of a project to perform the `scrapy crawl`action.

__Spiders__ folder
- It is the objects used to realise the scraping itself.
- we have to create `spider_*.py` files in this folder

__Project files__
- [items.py](link_to_template/items.py) : contains the structure of released items while scraping
- [settings.py](link_to_template/settings.py) : define parameters about crawling
- [middlewares.py](link_to_template/middlewares.py) : enhance the scraping process
- [pipelines.py](link_to_template/pipelines.py) : orchestrator of the scraping process 

## Custom files to leverage the scraping-corner 

__[run_spider.py](scrapy_project/run_spider.py)__
   
- It is used to run any spider from the repo with the following bash commande
  ```bash
  python run_spider.py -s SPIDER_ACRONYM
  ```
- the `SPIDER_ACRONYM` being a reference to the `spider_dispatch.json` configuration file.
- When running a spider, a new folder `scraped_data` will be created at the root of the `scraping` folder. Files will be saved in it.
- It is also possible to change the log level while crawling. The library used is [logzero](https://logzero.readthedocs.io/en/latest/), and loglevel (Debug/Info/Warn/Debug) are defined into spider class. Default value in here is `logger.INFO`
- Finally if you want a different start for the crawling, you will need to change the `self.start_urls` values, directly inside the spiders constructors.


__[count_line.py](scripts/count_line.py)__

- As running a spider might be very long (up to days if no limit is specified), this file will let you know the size of the file you are creating.
- Use the following command to get your answer :
    ```bash 
    python count_line.py scraped_data\your_file.py
    ```
__[jl_to_df.py](scripts/jl_to_df.py)__

- You will find here some lines to convert your `jl` file into a very manipulative pandas `DataFrame`. Which is much more convenient to perform Data Science analysis then !


## About scraped data

The `scraped_data` folder does not exist on the git repo and is specified into the `*.gitignore` file, so that it never appears. It will be automatically created during spider run. You will find your data into it.


## About Spider testing

As mentionned in the introduction
# Project list

## Amazon  
- Spider works
- Full project : Hackathon for XHEC students 2020
- Needs further processing
- Tried to scrap with Splash (useful lines still in spider and settings code)

## Booking
- Spider does not work

## Carrefour
- Uses Splash
- Working
- Code to imprve
## LBC : leboncoin
- Spider is working 80%
- Trying to repare buttemporary banned from LBC 
- UnitTesting in process (To be finished when ban is over or after using proxies)

## PV : ParuVendu
- Works Fine
- Logging not updated
- Code to clean
- No Unit Testing (not in a hurry as the structure as not changed in more than one year)
  
## SL : SeLoger
- Does not work : seems to be a lot of things to improve

## TA : TripAdvisor
- Multilple spiders
  - airlines : not working
  - hotels : not working
  - restaurant (information about restos) : working but quality to be imporved
  - restaurant (reviews of restos) : working but stops after few iterations (only 30k reviews for Paris => understand why)
## TrustPilot
- Some parts are working 


# Using Selenium

# Using Docker


# To-Do & Improvements
- Create the jl_to_df.py file
- Implement a possibility to select max_page (at each level)
- Add a config file to make it out of the scripts (start_urls would also be in it)
- Define and create an interface to select the preciously mentionned parameters and run spiders.


# Resources


- [Data Camp](https://www.datacamp.com/courses/web-scraping-with-python) : A course about how tu use scrapy
- [ParseHub](https://www.parsehub.com/) : a basic tool to realize scraping without coding
- [Selenium](https://selenium-python.readthedocs.io/) : a tool to simulate user interface
- [scraping wikipedia](https://fr.wikipedia.org/wiki/Web_scraping) : definitions about scraping
- [Scrapy website](https://scrapy.org/) : a huge treasure for scrapers 
-
- yielding multiple items in scrapy : https://stackoverflow.com/questions/39227277/can-scrapy-yield-different-kinds-of-items
- https://www.tutorialspoint.com/scrapy/scrapy_sending_e-mail.htm
- https://www.tutorialspoint.com/scrapy/index.htm