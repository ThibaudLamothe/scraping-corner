# Introduction

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

The main tool used to perform web scraping is `Scrapy`, a python library. (documentation [here](https://docs.scrapy.org/en/latest/))


Into the `scrapy_project` folder, are basically all the scrapy projects created with the `scrapy startproject project_name` command provided by the framework. The list of these project is described in a following section, with brief details for each of them. For the biggers one, I try to maintain a README file directly into the project folder.

## Default Scrapy files

When creating a new project with scrapy , it create a structure like the following : 

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

This configuration has the structure of an `INI file` and contains two sections which are `[settings]` and `[deploy]`.

Here to have multiple projects connected by a single configuration file.

__Spiders__ : There are the objects use to realise the scraping itself.
In this project, two spiders are availabe
- restoTAreview : get information for each reveiw of each
- restoTAinfo

__Project files__
- [items.py](scrapy_TA/items.py) : we create in here objects which will be used to store data
- [settings.py](scrapy_TA/settings.py) : define parameters about crawling (almost default parameters)
- [middlewares.py](scrapy_TA/middlewares.py) : original file
- [pipelines.py](scrapy_TA/pipelines.py) : original file  


## Custom files to leverage the scraping-corner 

__[run_spider.py](run_spider.py)__

__A. Setting up and running spider as is__
- `pip install -r requirements.txt`
- `python run_spider.py`

> `requirements.txt` file concern all the `nlp-datacamp`. Necessary libraries are `scrapy` and `logzero`.

__B. Parameters impacting crawling__
   
Two parameters will impact the execution of the `run_spider.py` script :
- `file_name`: the name of the `*.jl` file where data are saved
- `spider_name`: the name of the spider which will be run (there are 2 of them)

>When running a spider, a new folder `scraped_data` will be created at the root of the `scraping` folder. Files will be saved in it.


It is also possible to change the log level while crawling. The library used is [logzero](https://logzero.readthedocs.io/en/latest/), and loglevel (Debug/Info/Warn/Debug) are defined into spider class. Default value in here is `logger.INFO`

Finally if you want a different start for the crawling, you will need to change the `self.start_urls` values, directly inside the spiders constructors.


__[count_line.py](count_line.py)__

As running a spyder might be very long (up to days if no limit is specified), this file will let you know the size of the file you are creating.

Use the following command to get your answer :
```bash 
python count_line.py scraped_data\your_file.py
```
__[jl_to_df.py](jl_to_df.py)__

You will find here some lines to convert your `jl` file into a very manipulative pandas `DataFrame`. Which is much more convenient to realize Data Science then !

>Not created yet, function is already written somewhere on my computer, will add do this very soon :)


## About scraped data

This folder does not exist on the git repo and is specified into the `*.gitignore` file, so that it never appears.
It will be automatically created during spider run. You will find your files into it.


## About Spider testing

The second main folder here is the one to test spiders. Indeed sometimes the html structure of a website change and the selectors that we define might not be accurate in the future.

There is one file per spider :
- [test_resto.py](spider_testing/test_resto.py)
- [test_review.py](spider_testing/test_review.py)

> The tests are not yet available for now, only a basic request is done into `test_review.py`. Will be available in a further version.
> 

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


# Using Selenium
# Using Docker



# To-Do & Improvements
- Create the jl_to_df.py file
- Create test files (Ouptut a report - P1 is review, P2 is resto info)
- Modify selectors which are already old ones due to TA modifications
- Implement a possibility to select max_page (at each level)
- Implement a possibility to define 
- Add a config file to make it out of the scripts (start_urls would also be in it)
- Explore scrapy interface to run spiders
- Define and create a front to select the parameters evoked upper and run spiders.


# Resources


- [Data Camp](https://www.datacamp.com/courses/web-scraping-with-python) : A course about how tu use scrapy
- [ParseHub](https://www.parsehub.com/) : a basic tool to realize scraping without coding
- [Selenium](https://selenium-python.readthedocs.io/) : a tool to simulate user interface
- [scraping wikipedia](https://fr.wikipedia.org/wiki/Web_scraping) : definitions about scraping
- [Scrapy website](https://scrapy.org/) : a huge treasure for scrapers 

- yielding multiple items in scrapy : https://stackoverflow.com/questions/39227277/can-scrapy-yield-different-kinds-of-items
- https://www.tutorialspoint.com/scrapy/scrapy_sending_e-mail.htm
- https://www.tutorialspoint.com/scrapy/index.htm