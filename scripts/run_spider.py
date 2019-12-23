# Imports
import os
import time
import numpy as np


def print_execution_time(start):
    now = time.time()
    duree = np.round(now - start)
    duree_min = duree / 60
    print('Durée : {} min.'.format(duree_min))


if __name__ == "__main__":

    # Start script
    print('Start scrapping. (Be sure that Scrapy is locally installed in your environment)')
    start_time = time.time()
    if 'scrapped_data' not in os.listdir():
        os.mkdir('scrapped_data')

    # Parameters selection
    file_name = 'actu_x_summary_2.jl'
    spider_name = 'actuX_basic'

    # Execution of spider
    cmd = 'scrapy crawl {} -o ./scrapped_data/{}'.format(spider_name, file_name)
    os.system(cmd)
    print_execution_time(start_time)
