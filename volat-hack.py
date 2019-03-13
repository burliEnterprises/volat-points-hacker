"""
description & preamble:

this python script uses your browser to automatically log in and read articles on the page vol.at
(leading "news" site in vorarlberg(austria), consisting of 80 percent ads, 18 percent non-article-worthy posts and 2 percent real news)
it does this to earn you "points", which can then be used to get some free stuff

it requires you to have an account on the site, you have to create one manually beforehand and change those credentials at line 30-40
you will have to install a lot of packages via pip, i didn't put them in a extra file cause i ain't your fucking butler or some shit
install chromedriver at first too and change the path at line ~ 120 (search for "chrome" to find it)

why the fuck am i doing this? why the fuck not.
stupidity must be punished, that's why.
if you can't secure your site against a shitty, 19 year old script kiddie, who doesn't really know how to implement shit,
then you just deserve it, period.

enough talk. have fun :)
"""

#import mechanize

import requests
from datetime import datetime
from requests_html import HTMLSession   # request with POST function

import time     # used to sleep while site loads
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from bs4 import BeautifulSoup as bs

#from seleniumrequests import Chrome    # using pure selenium now
#from seleniumrequests import Firefox   # using pure selenium now

# vol.at credentials
username = "2pac4ever"
password = "admin123"

""" first option: mechanize
# didnt work cause you're not able to post requests
br = mechanize.Browser()
br.set_handle_robots(False)   # ignore robots
br.set_handle_refresh(False)  # can sometimes hang without this
url = "https://vol.at/"

'''response = br.open(url)
browser.select_form(nr = 0)
browser.form['username'] = "2pac4ever"
browser.form['password'] = "admin123"
browser.submit()
'''
"""

""" second option: requests
# in the terminal via requests (htmlrequests able to POST and get)
# didn't work cause ain't possible to send javascript to scroll down the page

# get timestamp for xml login request
now = datetime.now()
timestamp = datetime.timestamp(now)
# data sent to server for login:
payload = {
    'log': username,
    'password': password,
    'rememberme': 'true',
    'time': timestamp
}
request_login_url = 'https://www.vol.at/api/signon/login'

#with requests.session as s:
with HTMLSession() as s:
    p = s.post(request_login_url, data = {
        'log': username,
        'pwd': password,
        'rememberme': 'true',
        'time': '1552234004941'
    })
    # print the html returned or something more intelligent to see if it's a successful login page.
    print (p.text)

    # An authorised request.
    r = s.get('https://www.vol.at/profil')
    r = s.get('https://www.vol.at/news/vorarlberg')
    mail = r.html.find('.vodl-lead-flex-m__media')
    #print ('How many points you got? A lot.')
    print (mail)

    #print(r.html.absolute_links)

"""


# grab 25 article links of the site and put it in array
with HTMLSession() as s:

    r = s.get('https://www.vol.at/news/welt')
    mail = r.html.find('.vodl-lead-flex-m__media')

    #mail = mail[0].find('a')
    urls = []
    counter = 0
    print (len(mail))
    while counter < len(mail):
        x = str(mail[counter])
        y = x.split("href='")
        z = y[1].split("'")
        urls.append(z[0])
        counter = counter + 1
    print(urls)


""" third option: selenium
# opens chrome window so you can "watch" the whole process
# requires chromedriver to be installed on your machine
"""
browser = webdriver.Chrome("D:/Programmierung-Programme/chromedriver_win32/chromedriver.exe")
#browser = webdriver.Firefox("D:/Programmierung-Programme/geckodriver/geckodriver.exe")

# OG code:
# https://www.guru99.com/selenium-python.html
# https://selenium-python.readthedocs.io/locating-elements.html
browser.get("https://vol.at/")
show_login_form = browser.find_elements_by_class_name("vodl-login-label__login")
show_login_form[0].click()
time.sleep(5)

# fill in login form:
username = browser.find_elements_by_name("username")
password = browser.find_elements_by_name("password")
username[0].send_keys(username)
password[0].send_keys(password)
submit_that_thang = browser.find_elements_by_class_name("vodl-login__submit")
submit_that_thang[0].click()
time.sleep(5)


""" #xml request from chrome tools, shit ain't working for some reason ... only god knows i guess
response = webdriver.request('POST', request_login_url, data = {
    'log': username,
    'pwd': password,
    'rememberme': 'true',
    'time': timestamp
})
print(response) """

counter = 0     # to use different articles
counter2 = 0    # to count to 200
while counter2 < 200: # 200 request per hour as a maximum (high tech security by russmedia haha) .. used as endless loop
    browser.get(urls[counter])
    counter = counter + 1
    lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;") # scroll down
    if (counter == len(urls)):
        counter = 0
    time.sleep(2)   # otherwise vol.at point counter won't update
    if (counter2 == 199):
        time.sleep(2700)    # sleep for 45 minutes, 60 to much cause not all requests happen at the same time
        counter2 = 0
