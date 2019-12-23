import sys
import requests

sys.path.append('scrapy_TA/')
from spiders import get_info


# Use this link (all necessary elements)

url = "https://www.tripadvisor.co.uk/ShowUserReviews-g186338-d815603-r727250550-Tower_Tandoori-London_England.html"
response = requests.get(url)


url = get_info.get_review_url(response)
