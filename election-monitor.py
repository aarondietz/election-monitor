# -*- coding: utf-8 -*-
"""
Created on Sat Sep 15 17:19:10 2018

This is written to help monitor elections.

The idea is to record election result data over time so we can later analyze
trends to detect inconsistencies that may help us identify tampering, mistakes, 
or other impacts to an election.

The program will download a copy of an election result web page, at a timed
frequency. Later, we'll need to write data extraction code to get the data
into an analyzable format. As a worst case scenario, we could write these for
the few elections that are the most suspect. Best case scenario is to have 
enough volunteers to harvest nearly all our results in a mutually sharable
format, such that we could compare unusual results against the "norm" and/or
even recognize overall trends, should widescale tampering or other issues 
exist.


"""

# Import libraries
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone
import os.path
from apscheduler.schedulers.blocking import BlockingScheduler

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


# Add functionality to get the suffix of the retrieved web page (.html, .htm, .cfm, etc.)
# and then append that to the end of the saved copy.



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




# Establish the file name
file_name = "test" + "-" + loc_dt.strftime(fmt)
# Prepend the path
completePath = os.path.join(save_here, file_name + ".html")     

# Get unique page title from url to use as folder name to group all the retrieved copies
# in a single directory


# Function for storing the web site
# Got some of this code from: https://stackoverflow.com/questions/8024248/telling-python-to-save-a-txt-file-to-a-certain-directory-on-windows-and-mac
def store_copy(page_to_save, path_to_save_to):  
    # Open a file object for writing
    file_obj = open(path_to_save_to, "w")
    # Write the retrieved web page to the file object
    toFile = page_to_save
    file_obj.write(toFile)
    # Close the file object
    file_obj.close()



# Function where everything we need to repeat goes.
def repeat_tasks():
    # Call the function for saving a copy of the web page
    store_copy(html, completePath)


# Repeat the retrieval according to the frequency set
# code snippet originally from: https://stackoverflow.com/questions/22715086/scheduling-python-script-to-run-every-hour-accurately
# link to documentation: https://apscheduler.readthedocs.io/en/latest/ 
scheduler = BlockingScheduler()
scheduler.add_job(repeat_tasks, 'interval', minutes = frequency)
scheduler.start()





# To do list that might not be tracked anywhere else:
#
# Add functionality for capturing various different URL suffixes (html, pdf, etc.) and saving as such.
# Add functionality for each page to be saved in its own folder (for when it can handle more than one page)





#### IDEAS - PROBABLY BAD ONES

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




































