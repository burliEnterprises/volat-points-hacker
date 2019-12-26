#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import configparser
import io
import gzip
import json

import logging
import os

import requests
import time
from datetime import datetime

from requests_html import HTMLSession   # needed to grab articles, request with POST function
from selenium import webdriver  # web scraper
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import webbrowser   #for github button action, to open browser


class HackingShit:

    # constructor, needed? dunno
    def __init__(self, _username, _password):
          self.username = _username
          self.password = _password

    # Do the magic and add points via selenium etc
    def hackThemPoints(self):
        # grab 25 article links of the site and put it in array
        # grab 1 video link from homepage --> In Selenium not implemented yet
        with HTMLSession() as s:
            r = s.get('https://www.vol.at/news/welt')
            #mail = r.html.find('.vodl-lead-flex-m__media')
            mail = r.html.find('.vodl-media')
            urls = []
            counter = 0
            print (len(mail))
            while counter < len(mail):
                x = str(mail[counter])
                y = x.split("href='")   
                print(y)
                z = y[1].split("'")
                if z[0].find("vol.at") == -1:
                    # other url like vn.at redirect, dont add 
                    print("other url")
                else:
                    urls.append(z[0])
                counter = counter + 1
            print(urls)
        #selenium
        # opens chrome window so you can "watch" the whole process
        # requires chromedriver to be installed on your machine

        #local webdriver, exe in directory, else path:
        # webdriver must fit chrome version, download here https://chromedriver.chromium.org/downloads
        browser = webdriver.Chrome("chromedriver.exe")

        """heroku config, buildpacks installed already and path variables set
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.binary_location = "/app/.apt/usr/bin/google-chrome-stable"
        browser = webdriver.Chrome(executable_path='/app/.chromedriver/bin/chromedriver', chrome_options=chrome_options)"""

        # OG code:
        # https://www.guru99.com/selenium-python.html
        # https://selenium-python.readthedocs.io/locating-elements.html

        ### LOGIN:

        browser.get("https://vol.at/")
        show_login_form = browser.find_elements_by_class_name("vodl-login-label__login")
        show_login_form[0].click()
        time.sleep(5)

        # fill in login form and click login button:
        username = browser.find_elements_by_name("username")
        password = browser.find_elements_by_name("password")
        username[0].send_keys(self.username)    # from constructor
        password[0].send_keys(self.password)
        submit_that_thang = browser.find_elements_by_class_name("vodl-login__submit")
        submit_that_thang[0].click()
        time.sleep(5)

        # check if login successful or failed --> fail, return
        try:
            errormessage_div =  browser.find_elements_by_class_name("vodl-login__error")[0].text
            browser.quit()
            return "Login failed! Check your credentials before trying again!"
        #if "name" in errormessage_div:
        except IndexError:
            print ("login successful")


        ### GAIN POINTS:

        article_counter = 0          # to use different articles, array index
        still_gaining_points = 1    # 1 yes, 0 nope --> break loop
        total_points = 0            # current points, checks if points are still adding
        starting_points = 0          # points when script starts
        first_iteration = 1         # 1 yes to get starting points, 0 afterwards

        while still_gaining_points == 1:     # 200 request per day as a maximum (high tech security by russmedia haha) .. used as endless loop if i wanted to run it a week w/o stopping the script

            # load page and scroll down:
            print(str(len(urls)))
            if (article_counter >= len(urls)):      # reset array index, open all articles 2nd time, 3rd time, ...
                article_counter = 0
            browser.get(urls[article_counter])
            lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            print("scrolled down")
            time.sleep(2)         # otherwise vol.at point counter won't update

            # get current points and
            volat_points_text =  browser.find_elements_by_class_name("points")[0].text
            x = ''.join(i for i in volat_points_text if i.isdigit())
            new_total_points = int(x)

            # if points weren't added (means that article has been read to often --> remove from articles array, continue program cause other articles will still add points)
            if new_total_points <= total_points:
                if len(urls) <= 1:    # no more articles left after this one --> break loop
                    still_gaining_points = 0
                else:      # remove from array, article dead
                    urls.remove( urls[article_counter] )

            # get points the user starts with in first loop iteration
            if first_iteration == 1:
                starting_points = new_total_points
                print( "You started with "+ str(starting_points) + " Points!" )
                first_iteration = 0
            else:
                print( "User got "+ str(new_total_points) + " Points now!" )        # print current points

            total_points = new_total_points    # update total points to check in next iteration

            article_counter += 1

        # post loop, show message box how many points have been added:
        points_added = total_points - starting_points
        browser.quit()
        res = str(points_added) + " Points added!", "Everything went smoothly :)"
        return res



# how to implement pyguru: https://github.com/alejandroautalan/pygubu/wiki/CommandProperties
# tk for gui, gui made in gui builder "pygubu" --> pygubu-designer to open it in win search
# gui runs in this class
try:
    import tkinter as tk  # for python 3
    from tkinter import messagebox
except:
    import Tkinter as tk  # for python 2
    import tkMessageBox as messagebox
import pygubu

class Application:

    # constructor, code copied
    def __init__(self, master):
        #1: Create a builder
        self.builder = builder = pygubu.Builder()
        #2: Load an ui file
        builder.add_from_file('volat-ui.ui')
        #3: Create the widget using a master as parent
        self.mainwindow = builder.get_object('toplevel_ui', master)
        builder.connect_callbacks(self)

    # button: hacking
    def start_hacking(self):
        # create class object for the selenium part and run method
        user = self.builder.tkvariables.__getitem__('inp_str_username').get()
        pwd = self.builder.tkvariables.__getitem__('inp_str_password').get()

        print ('Username is ' + user )
        print ('Password is ' + pwd )

        hackIt = HackingShit(user, pwd)
        result = hackIt.hackThemPoints()

        messagebox.showinfo("Attention", str(result) )

    # button: github
    def go_github(self):
        # open browser and show github repo why not
        print("go github clicked")
        url_repo = "https://github.com/burliEnterprises/volat-points-hacker"
        webbrowser.open(url_repo)

# Show GUI
if __name__ == '__main__':
    print("cups of the rose, b's in my old phone ...")
    root = tk.Tk()
    root.title('VolAT-Points-Hacker')
    app = Application(root)
    root.mainloop()
