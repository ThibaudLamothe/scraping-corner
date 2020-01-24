# Imports
import os
import sys
import time
import numpy as np


def print_execution_time(start):
    now = time.time()
    duree = now - start
    duree_min = np.round(duree / 60, 2)
    print('Durée : {} min.'.format(duree_min))


def get_LBC():
    file_name = 'LBC_corner.jl'
    spider_name = 'spiderLBC'
    project_name = 'LBC'
    return file_name, spider_name, project_name


def get_SL():
    file_name = 'SL_corner.jl'
    spider_name = 'spiderSL'
    project_name = 'SL'
    return file_name, spider_name, project_name


def get_TA():
    file_name = 'TA_corner.jl'
    spider_name = 'spiderTA'
    project_name = 'TA'
    return file_name, spider_name, project_name


def get_PV():
    file_name = 'PV_corner.jl'
    spider_name = 'spiderPV'
    project_name = 'PV'
    return file_name, spider_name, project_name


def get_X_basic():
    file_name = 'actu_x_summary_2.jl'
    spider_name = 'actuX_basic'
    project_name = 'XHEC'
    return file_name, spider_name, project_name


def get_TrustPilot():
    file_name = 'TP_corner.jl'
    spider_name = 'pilot'
    project_name = 'TrustPilot'
    return file_name, spider_name, project_name


def get_TA_airline():
    file_name = 'TA_airline_corner.jl'
    spider_name = 'airlineTA'
    project_name = 'TA'
    return file_name, spider_name, project_name


def get_booking():
    file_name = 'booking_corner.jl'
    spider_name = 'BookingSpider'
    project_name = 'Booking'
    return file_name, spider_name, project_name


def dispatcher(name):
    switcher = {
        'LBC': get_LBC,
        'TA': get_TA,
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December"
    }
    my_function = switcher.get(name, "Invalid Spider")
    return my_function


if __name__ == "__main__":
    print(sys.argv)
    # Get eventual arguments
    get_parameters = None
    for arg in sys.argv:
        get_parameters = dispatcher('LBC')
    if get_parameters is None:
        get_parameters = get_booking

    # Start script
    print('Start scrapping. (Be sure that Scrapy is locally installed in your environment)')

    # Prepare storage
    if 'scrapped_data' not in os.listdir('../'):
        os.mkdir('../scrapped_data')

    # Parameters selection
    file_, spider, project = get_parameters()
    os.environ['SCRAPY_PROJECT'] = project

    # Execution of spider
    start_time = time.time()
    cmd = 'scrapy crawl {} -o ../scrapped_data/{}'.format(spider, file_)
    os.system(cmd)
    print_execution_time(start_time)
