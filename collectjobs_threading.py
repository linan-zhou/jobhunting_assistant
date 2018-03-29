from selenium import webdriver
import re
import time
import urllib
import random
import pymysql
import threading

global updatetime
updatetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

lock = threading.Lock()

def get_jd_info(urlstring, id):
    lock.acquire()
    jddr = webdriver.Chrome()
    jddr.get(urlstring)
    company = jddr.find_element_by_class_name('company').text
    jobtitle = jddr.find_element_by_class_name('job-name').get_attribute('title')
    jobdescription = jddr.find_element_by_class_name('job_bt').text
    workaddress = jddr.find_element_by_class_name(' work_addr').text
    cur.execute('''
                        INSERT INTO lagoujobs (id, company, jobtitle, jd, address, updatetime)
                        VALUES (%s, %s, %s, %s, %s, %s)''',
                (id, company, jobtitle, jobdescription, workaddress, updatetime))
    a = random.uniform(5, 10)
    print('sleep:', a)
    time.sleep(a)
    lock.release()

def collet_from_one_page(driver):
    wb_links_elements = driver.find_elements_by_class_name('position_link')
    wb_links = []
    for lk in wb_links_elements:
        wb_links.append(lk.get_attribute('href'))
    print(wb_links)
    jdthreading = []
    for urlstring in wb_links:
        id = re.search(r'https://www.lagou.com/jobs/([0-9]*).html', urlstring).group(1)
        if cur.execute('''SELECT id from lagoujobs WHERE id = %s''', id):
            continue
        jdnow = threading.Thread(target=get_jd_info, args=(urlstring, id,))
        jdthreading.append(jdnow)
        jdnow.start()
        print('id:', id)
    for jdnow in jdthreading:
        jdnow.join()


if __name__ == '__main__':
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='mysql', charset='utf8')
    cur = conn.cursor()
    cur.execute("USE jobhunting")

    ex = urllib.parse.quote('不要求')
    xl = urllib.parse.quote('本科')
    city = urllib.parse.quote('北京')
    url = 'https://www.lagou.com/jobs/list_Python?px=new&gj={}&xl={}&city={}#order'.format(ex, xl, city)
    driver = webdriver.Chrome()
    driver.get(url)
    collet_from_one_page(driver)
    next_icon = driver.find_element_by_class_name('pager_next')
    now = 1
    while next_icon:
        print(now, ' ', next_icon.text)
        try:
            last_icon = driver.find_element_by_class_name('pager_next_disabled')
            break
        except :
            time.sleep(3)
            next_icon.click()
            time.sleep(3)
            collet_from_one_page(driver)
            now += 1
            print(now)
            next_icon = driver.find_element_by_class_name('pager_next')
            print('a loop finished')

    cur.connection.commit()
    cur.close()
    conn.close()
