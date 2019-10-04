#!/usr/bin/env python
# -*- coding: utf-8 -*-

# copied from nba app:

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

import sys
import configparser
import io
import urllib.request
import urllib.parse
import urllib.error
import gzip
import json


try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

import logging
import os
from flask import Flask, render_template
from flask import request
from flask import make_response

# my own shit:

import requests
import time
from datetime import datetime

from requests_html import HTMLSession   # request with POST function
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Flask app should start in global layout
app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)


def removeQuotesFromValue(value):
	value = value.replace("'", '"')
	# value = value.replace('"', "")
	return value

def splitLineIntoParts(line):
	line = line.lstrip()
	line = line.rstrip()
	line = removeQuotesFromValue(line)
	line = line.split("=", 1)
	return line


with open('.env') as e:
	for line in e:
		l = splitLineIntoParts(line)
		if (len(l) > 1):
			name = l[0]
			value = l[1]
			print()
            os.system('heroku config:set GOOGLE_CHROME_BIN=/app/.apt/usr/bin/google_chrome')
            os.system('heroku config:set CHROMEDRIVER_PATH=/app/.chromedriver/bin/chromedriver')



# vol.at credentials
__username = "2pac4ever"
__password = "admin123"




@app.route('/hacking', methods=['GET'])
def hackThemPoints():

    # grab 25 article links of the site and put it in array
    # grab 1 video link from homepage
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



    """ selenium
    # opens chrome window so you can "watch" the whole process
    # requires chromedriver to be installed on your machine
    """
    #lokal:
    #browser = webdriver.Chrome("D:/WebProjects/vol-at-hacking-points/volat-points-hacker/chromedriver.exe")

    #heroku config, buildpacks installed already and path variables set
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.binary_location = GOOGLE_CHROME_PATH
    browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
    # OG code:
    # https://www.guru99.com/selenium-python.html
    # https://selenium-python.readthedocs.io/locating-elements.html

    ### LOGIN
    browser.get("https://vol.at/")
    show_login_form = browser.find_elements_by_class_name("vodl-login-label__login")
    show_login_form[0].click()
    time.sleep(5)

    # fill in login form:
    username = browser.find_elements_by_name("username")
    password = browser.find_elements_by_name("password")
    username[0].send_keys(__username)
    password[0].send_keys(__password)
    submit_that_thang = browser.find_elements_by_class_name("vodl-login__submit")
    submit_that_thang[0].click()
    time.sleep(5)

    counter = 0     # to use different articles
    counter2 = 0    # to count to 200
    """while counter2 < 199: # 200 request per day as a maximum (high tech security by russmedia haha) .. used as endless loop if i wanted to run it a week w/o stopping the script
        browser.get(urls[counter])
        counter = counter + 1
        lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;") # scroll down
        if (counter == len(urls)):
            counter = 0
        time.sleep(2)   # otherwise vol.at point counter won't update
        if (counter2 == 199):
            time.sleep(86400)    # sleep for 24 hours
            counter2 = 0"""

    res = json.dumps({"what's up ": "a lot"})
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r



##### FLASK CONFIG #####
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5555))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
    #app.run(debug=False, port=port, host='127.0.0.1')
