# -*- coding: utf-8 -*-
"""
Created on Sat Sep 15 17:19:10 2018


"""

# Import libraries
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone
import os.path

# Add functionality for dialog box GUI


# Add functionality for building into an executable that can be 
# run by any ol' person


# Add functionality for getting more than one page


# Ask what web page to get
url = "http://example.com"

# Ask where to store the file/s
# Directory must already exist
save_here = 'C:/monitor/'


# Set the retrieval frequency (in minutes)
frequency = 5.0


# Add a "Stop" button


# Add a "Stop after x times" feature or at specific time of day

    
# Get the web page
html = requests.get(url).text
print (html)



# Get timestamp - all timestamps will be Eastern time for consistency,
# in case later we want to stitch data from many users together in time
# Code grabbed from https://stackoverflow.com/questions/34549663/how-to-set-timezone-to-eastern-for-datetime-module-in-python
# define date format, example: 2015-12-31 19:21:00 EST-0500
fmt = '%Y%m%d%H%M%S%Z%z'
# define eastern timezone
eastern = timezone('US/Eastern')
# localized datetime
loc_dt = datetime.now(eastern)
# print(loc_dt.strftime(fmt))



# Store the web site
# Got some of this code from: https://stackoverflow.com/questions/8024248/telling-python-to-save-a-txt-file-to-a-certain-directory-on-windows-and-mac

# Establish the file name
file_name = "test" + "-" + loc_dt.strftime(fmt)
# Get unique page title from url to use as folder name to group all the retrieved copies
# in a single directory

# Prepend the path
completePath = os.path.join(save_here, file_name + ".html")         
# Open a file object for writing
file_obj = open(completePath, "w")
# Write the retrieved web page to the file object
toFile = html
file_obj.write(toFile)
# Close the file object
file_obj.close()



# Repeat the retrieval according to the frequency set







# To do:
#
# Add functionality for capturing various different URL suffixes (html, pdf, etc.) and saving as such.
# Add functionality for each page to be saved in its own folder





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




































