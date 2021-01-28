# Imports
import os
import json
import time
import argparse
import numpy as np


# To evaluate scraping execution time
def print_execution_time(start):
    now = time.time()
    duree = now - start
    duree_min = np.round(duree / 60, 2)
    print('Durée : {} min.'.format(duree_min))


# To parse which spider is called
def get_sigle():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--spider", help="Define the sigle to get into the config file")
    args = parser.parse_args()
    if args.spider:
        return args.spider
    return "EXP"

# To get the config of the spider to call
def get_config(dispatcher_path, sigle):
    with open(dispatcher_path) as json_file:
        data = json.load(json_file)
    if sigle not in data.keys():
        return None, None, None, None

    file_name = data[sigle]['file_name']
    spider_name = data[sigle]['spider_name']
    project_name = data[sigle]['project_name']
    test_spiders = None
    if 'test' in data[sigle].keys():
        test_spiders = data[sigle]['test']
    return file_name, spider_name, project_name, test_spiders


if __name__ == "__main__":

    # Start script
    print('Start scrapping. (Be sure that Scrapy is locally installed in your environment)')

    # Prepare storage
    if 'data' not in os.listdir('../'):
        os.mkdir('../data')
        os.mkdir('../data/corner_test')

    # Get the spiders parameters
    file_, spider, project, test_spiders = get_config(
        dispatcher_path='spider_dispatch.json',
        sigle=get_sigle()
    )

    # Set os information for default scrapy project (link with the scrapy.cfg file)
    os.environ['SCRAPY_PROJECT'] = project

    # Making tests before running spiders
    if test_spiders is not None:
        for test in test_spiders:
            cmd = 'scrapy crawl {}'.format(test)
            os.system(cmd)

    # Start chronometer
    start_time = time.time()

    # Run spider
    cmd = 'scrapy crawl {} -o ../data/corner_test/{}'.format(spider, file_)
    os.system(cmd)

    # Display execution time
    print_execution_time(start_time)
