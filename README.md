# VolAT Points Hacker
![hacking cat](https://media.giphy.com/media/o0vwzuFwCGAFO/giphy.gif)
Hello there 😊 I'd like to thank you for making the time to look at my code instead of doing something reasonable like spending money on Wish (have you heard of [WishWiz](https://chrome.google.com/webstore/detail/the-wishwiz/lkijfedegilaikaacnoblhekmlegpeln)?) or listening to the new Rebecca Black album. I greatly apprectiate your efforts!

I'd also like to thank Russmedia for making all of this possible. This wouldn't have been possible without your crappy programming and low level security 😉

## Description:

This tool basically allows you to craft *Ländepunkte* on the Vorarlberger "news" page *Vorarlberg Online (vol.at).*
In case you don't know: Vorarlberg Online is the leading online platform in the area, although it actually consists of about 80% ads, 19% weird but funny comments & 1% news-worthy posts.

You can use your earned points to get free stuff like mugs, towels, vouchers & bags. Visit their page to see the full selection of gifts.

## Prerequisites:

Although a GUI etc. is included in the program, you will need to install some weird looking things beforehand on your own.
*Important: If you don't use Windows, the program might or might not work, but ... well ... go figure it out on your own haha shouldn't have bought that overpriced thing with half an apple on it* 😘

**1. Download & Install Python:**
 You'll need to install Python3 on your local machine. If you don't know how to do that, have a look [here](https://realpython.com/installing-python/).

 **2. Install a few packages:**
 After installing Python, you'll need to add some packages to your python installation. Open you command line by typing `cmd` in the Windows search box and type the following:

    pip install requests
    pip install requests-html
    pip install selenium
    pip install pygubu

 **3. Download or clone this repository**
 You'll need to get my code on your machine. Either clone the repo by using Git or simply download it by clicking the green button above (unzip it too, once the download is completed!)

 ## Usage:
 Once everything is set up, we're good to go. Double click on the file `execute_program.bat` and the program will open. Simply enter your login credentials into the beautifully designed GUI 🤮 to start the magic :)

## Don't read if you can't code 😉:

How many points can you earn a day?
- You can share 2 articles per social platform --> 4 platforms x 2 articles x 5 points/each = 40 points
- You can read 200 articles --> 200 articles x 3 points = 600 points
- You can click on 20 videos on the main page --> 20 videos x 5 points = 100 points
--
740 points per day are possible to make this way.
-----
There is also a way to earn more than 10.000 points per day by using a combination of login & logout. You'll receive 10 points simply for logging into the site. They will set a cookie, you could forgo that by using Chromedriver and by closing & opening the browser again once you've logged in.

Unfortunately it is not possible to use those points. Another great developer and mastermind 😊 got his account blocked once he tried to use his points. If you're interested in his code anyways, have a look at his [code](https://github.com/Moon36/volat-point-farm).
