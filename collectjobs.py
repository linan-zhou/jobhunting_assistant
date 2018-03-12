from selenium import webdriver
import re
import time
import urllib
import random
import requests
from bs4 import BeautifulSoup

ex = urllib.parse.quote('不要求')
xl = urllib.parse.quote('本科')
city = urllib.parse.quote('北京')
url = 'https://www.lagou.com/jobs/list_Python?px=new&gj={}&xl={}&city={}#order'.format(ex, xl, city)
driver = webdriver.Chrome()
driver.get(url)
wb_links_elements = driver.find_elements_by_class_name('position_link')
wb_links = []
for lk in wb_links_elements:
    wb_links.append(lk.get_attribute('href'))
ids = []
company = []
jobtitle = []
jobdescription = []
workaddress = []
jddr = webdriver.Chrome()
print(wb_links)
for urlstring in wb_links:
    ids.append(re.search(r'https://www.lagou.com/jobs/([0-9]*).html', urlstring).group(1))
    jddr.get(urlstring)
    company.append(jddr.find_element_by_class_name('company').text)
    jobtitle.append(jddr.find_element_by_class_name('job-name').get_attribute('title'))
    jobdescription.append(jddr.find_element_by_class_name('job_bt').text)
    workaddress.append(jddr.find_element_by_class_name('work_addr').text)
    a = random.uniform(10, 15)
    time.sleep(a)



