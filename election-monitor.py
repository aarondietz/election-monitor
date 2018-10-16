# -*- coding: utf-8 -*-
"""
Created on Sat Sep 15 17:19:10 2018


"""

# Import libraries
import requests
from bs4 import BeautifulSoup


# Add functionality for dialog box GUI


# Add functionality for building into an executable that can be 
# run by any ol' person


# Add functionality for getting more than one page


# Ask what web page to get
url = "http://example.com"

# Ask where to store it

    
# Get the web page
html = requests.get(url).text
print (html)


# Store the web site
# Add timestamp to file name









#### IDEAS - PROBABLY BAD ONES
"""
import wget
from bs4 import BeautifulSoup
url = "https://www.facebook.com/hellomeets/events"

down = wget.download(url)

f = open(down, 'r')
htmlText = "\n".join(f.readlines())
f.close()
print htmlText






This is an example using pythons built in urllib2:

import urllib2
from bs4 import BeautifulSoup
url = "https://www.facebook.com/hellomeets/events"

html = urllib2.urlopen(url).read()
print html
"""



# Use cron with wget
# http://www.scrounge.org/linux/cron.html 

"""

# Source: https://stackoverflow.com/questions/1367189/how-to-download-a-webpage-in-every-five-minutes
# This is working but I don't know where it's saving.
import time
import os

wget_command_string = "wget www.aarondietz.us"

while True:
    os.system(wget_command_string)
    time.sleep(5*60)

"""

"""
# This stuff is to schedule the grabbing of the site's content.

# code snippet originally from: https://stackoverflow.com/questions/22715086/scheduling-python-script-to-run-every-hour-accurately
# link to documentation: https://apscheduler.readthedocs.io/en/latest/ 
from apscheduler.schedulers.blocking import BlockingScheduler

def some_job():
    print ("Job happens")

scheduler = BlockingScheduler()
scheduler.add_job(some_job, 'interval', minutes = 1)
scheduler.start()




# To shut it down:
# scheduler.shutdown()
"""




































