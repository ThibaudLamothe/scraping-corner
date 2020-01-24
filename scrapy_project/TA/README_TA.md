This Scrapping module runs with TripAdvisor

Set up and running spider as is
pipenv install Pipfile
pipenv run python run_spider.py
Modifications available
Change log level in settings.py l.17
Change printing infomation in spiders (function )
Select file name for scrapped data into scrapped_data folder
Select spider to run
Different spiders
restoTAcomment
restoTAinfo
restoTAreviewer (not written as for now)
hotelTA (from tclavier, not updated)
airlineTA (from mcriom, not updated)