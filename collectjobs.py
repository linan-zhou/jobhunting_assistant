from selenium import webdriver
import re
import time
import urllib
import random
import requests
from bs4 import BeautifulSoup
import pymysql


conn = pymysql.connect(host='localhost', user='root', passwd='', db='mysql', charset='utf8')
cur = conn.cursor()
cur.execute("USE jobhunting")

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
# ids = []
# company = []
# jobtitle = []
# jobdescription = []
# workaddress = []
jddr = webdriver.Chrome()
print(wb_links)
for urlstring in wb_links:
    id = re.search(r'https://www.lagou.com/jobs/([0-9]*).html', urlstring).group(1)
    # ids.append(id)
    if cur.execute('''SELECT id from lagoujobs WHERE id = %s''', id):
        continue
    jddr.get(urlstring)
    print('id:', id)
    company = jddr.find_element_by_class_name('company').text
    jobtitle = jddr.find_element_by_class_name('job-name').get_attribute('title')
    jobdescription = jddr.find_element_by_class_name('job_bt').text
    workaddress = jddr.find_element_by_class_name(' work_addr').text
    cur.execute('''
                INSERT INTO lagoujobs (id, company, jobtitle, jd, address)
                VALUES (%s, %s, %s, %s, %s)''',
                (id, company, jobtitle, jobdescription, workaddress))
    a = random.uniform(5, 10)
    print('sleep:', a)
    time.sleep(a)

cur.connection.commit()
cur.close()
conn.close()



