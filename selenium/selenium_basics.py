from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

######################################################
######################################################
#                     Chrome driver
######################################################
######################################################

# https://sites.google.com/a/chromium.org/chromedriver/downloads
path = '/Users/thibaud/Downloads/chromedriver'
browser = webdriver.Chrome(path)

######################################################
######################################################
#                     Elementary action
######################################################
######################################################

# Logging to url
url = 'https://www.tripadvisor.fr/'
browser.get(url)

# Test to find an element
elem = browser.find_element_by_link_text('Restaurants')
elem.get_attribute('href')
elem.click()

# Fulfilling a searchobox
searchbar = browser.find_element_by_class_name('q')
searchbar.send_keys('Paris')
searchbar.send_keys(Keys.ENTER)


# Wait for an element to appear before making action
elmt = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "reaction-item__text")))

# Scrolling
browser.execute_script("window.scrollTo(0, Y)") 

# Inteeracting between multiple windows (in case of dialog box)
original_window =  browser.window_handles[0]
browser.switch_to_window(original_window)

# Geet all attributes
# attrs = bs.driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', radio)

######################################################
######################################################
#               Acting like a human
######################################################
######################################################

USER_AGENT = 'Mozilla/5.0 (Linux; Android 7.0; SM-G930VC Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/58.0.3029.83 Mobile Safari/537.36'
PROXY = "157.230.251.216:80"

opts = Options()
opts.add_argument(USER_AGENT)
opts.add_argument('--proxy-server=%s' % PROXY)

path = '/Users/thibaud/Downloads/chromedriver'
driver = webdriver.Chrome(path) #, options=opts)

url = 'https://www.leboncoin.fr/electromenager/1765849788.htm/'
driver.get(url)