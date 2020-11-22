# Introduction

__This part of the course concerns Data Extraction : we scrap restaurant data from TripAdvisor.__

This folder contains 3 folders and 3 scripts
- [run_spider.py](run_spider.py): run this one to start scrapping (see how to later ;)) 
- [count_line.py](count_line.py) : while scrapping can give an idea of the number of item already stored.
- [jl_to_df.py](jl_to_df.py) : output file is a `jl` file. This is a script to read a `jl` file and transform it into a `pandas DataFrame`
- `scrapy_TA`: contains the `scrapy` project and the `spiders` 
- `spider_testing` : contains files to test the html/css selectors used in spiders
- `scrapped_data` : will be created automatically when spider is run

A better description of all of them is availabe right now ! Enjoy :) !

# Single scripts

__[run_spider.py](run_spider.py)__

__A. Setting up and running spider as is__
- `pip install -r requirements.txt`
- `python run_spider.py`

> `requirements.txt` file concern all the `nlp-datacamp`. Necessary libraries are `scrapy` and `logzero`.

__B. Parameters impacting crawling__
   
Two parameters will impact the execution of the `run_spider.py` script :
- `file_name`: the name of the `*.jl` file where data are saved
- `spider_name`: the name of the spider which will be run (there are 2 of them)

>When running a spider, a new folder `scrapped_data` will be created at the root of the `scrapping` folder. Files will be saved in it.


It is also possible to change the log level while crawling. The library used is [logzero](https://logzero.readthedocs.io/en/latest/), and loglevel (Debug/Info/Warn/Debug) are defined into spider class. Default value in here is `logger.INFO`

Finally if you want a different start for the crawling, you will need to change the `self.start_urls` values, directly inside the spiders constructors.


__[count_line.py](count_line.py)__

As running a spyder might be very long (up to days if no limit is specified), this file will let you know the size of the file you are creating.

Use the following command to get your answer :
```bash 
python count_line.py scrapped_data\your_file.py
```
__[jl_to_df.py](jl_to_df.py)__

You will find here some lines to convert your `jl` file into a very manipulative pandas `DataFrame`. Which is much more convenient to realize Data Science then !

>Not created yet, function is already written somewhere on my computer, will add do this very soon :)

# Scrapy 

The selected tool to perform web scraping is `Scrapy`, a python librarie (documentation [here](https://docs.scrapy.org/en/latest/)).

All the files here come from scrapy framework :

- [items.py](scrapy_TA/items.py) : we create in here objects which will be used to store data
- [settings.py](scrapy_TA/settings.py) : define parameters about crawling (almost default parameters)
- [middlewares.py](scrapy_TA/middlewares.py) : original file
- [pipelines.py](scrapy_TA/pipelines.py) : original file

__Spiders__ : There are the objects use to realise the scrapping itself.
In this project, two spiders are availabe
- restoTAreview : get information for each reveiw of each
- restoTAinfo


# Spider testing

The second main folder here is the one to test spiders. Indeed sometimes the html structure of a website change and the selectors that we define might not be accurate in the future.

There is one file per spider :
- [test_resto.py](spider_testing/test_resto.py)
- [test_review.py](spider_testing/test_review.py)

> The tests are not yet available for now, only a basic request is done into `test_review.py`. Will be available in a further version.

# Scrapped data

This folder does not exist on the git repo and is specified into the `*.gitignore` file, so that it never appears.
It will be automatically created during spider run. You will find your files into it.

Then, as this folder is only reserved to scrapping, you will find cleaning, EDA and basic pre-processing [here](../cleaning/README.md).


# To-Do & Improvements
- Create the jl_to_df.py file
- Create test files (Ouptut a report - P1 is review, P2 is resto info)
- Modify selectors which are already old ones due to TA modifications
- Implement a possibility to select max_page (at each level)
- Implement a possibility to define 
- Add a config file to make it out of the scripts (start_urls would also be in it)
- Explore scrapy interface to run spiders
- Define and create a front to select the parameters evoked upper and run spiders.

# To go further

Here are some links related to scrapping, that you could use 
- [Data Camp](https://www.datacamp.com/courses/web-scraping-with-python) : A course about how tu use scrapy
- [ParseHub](https://www.parsehub.com/) : a basic tool to realize scrapping without coding
- [Selenium](https://selenium-python.readthedocs.io/) : a tool to simulate user interface
- [Scrapping wikipedia](https://fr.wikipedia.org/wiki/Web_scraping) : definitions about scrapping
- [Scrapy website](https://scrapy.org/) : a huge treasure for scrapers 