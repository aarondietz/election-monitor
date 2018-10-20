# -*- coding: utf-8 -*-
"""
Created on Sat Sep 15 17:19:10 2018

This is written to help monitor elections.

Written on Python 3.6.4

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
from apscheduler.schedulers.background import BackgroundScheduler



# Set what web page to get
# Future functionality should ask what page to get
url = "http://example.com"


# Set where to store the file/s
# Directory must already exist
save_here = 'C:/monitor/'
# Future functionality should ask where to save to
# Future functionality should also use unique web page title from url stored
# to use as a folder name to group all the retrieved copies in a single directory


# Set the retrieval frequency (in minutes) / how often 
# to retrieve a copy of the site
# Future functionality should ask the frequency
frequency = 5.0



# Set how long the program will run for.
# Run the program this number of times / save this number of copies and then quit
number_of_copies = 144


# Initialize variable to keep track of how many times its run/how many copies saved
copies_saved = 0


# Establish what we'll call the saved version of the file
# Future functionality should just grab the web page title and use that
# with remediation for duplicates (so if we've already grabbed a page titled 
# that, it'll add a version number or do some other remediation)
filename = "election_result"




    
# Get the web page
def get_web_page(url_string):
    file_obj = requests.get(url).text
    #print (file_obj)
    return file_obj
    # Future functionality should get the suffix of the retrieved web page (.html, .htm, .cfm, etc.)
    # and then keep that to append to the end of the saved copy.


# Function only used when called by create_path()
def get_time_stamp():
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
    return loc_dt.strftime(fmt)



def create_path(filename_string, save_path):
    # Add the time stamp to the filename
    #filename_w_time = filename + "-" + loc_dt.strftime(fmt)
    filename_w_time = filename_string + "-" + get_time_stamp()
    # Prepend the path
    return os.path.join(save_path, filename_w_time + ".html")     




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
    html = get_web_page(url)
    save_path = create_path(filename, save_here)
    store_copy(html, save_path)
    global copies_saved
    copies_saved += 1
    # Need a more graceful way to stop the scheduler; this throws an error
    if copies_saved == number_of_copies:
        scheduler.shutdown()


# Repeat the retrieval according to the frequency chosen above
# code snippet originally from: https://stackoverflow.com/questions/22715086/scheduling-python-script-to-run-every-hour-accurately
# link to documentation: https://apscheduler.readthedocs.io/en/latest/ 
scheduler = BlockingScheduler()   
scheduler.add_job(repeat_tasks, 'interval', minutes = frequency)
scheduler.start()




### TO DO LIST ###
# Add functionality for capturing various different URL suffixes/page types (html, pdf, etc.) and saving as such.

# Add functionality for dialog box GUI (goal is to make it easy for non-coders to use)

# Add functionality for building into an executable that can be run by non-coders

# Add functionality for getting more than one page
# Add functionality for each page to be saved in its own folder (for when it can handle more than one page)

# Add a "Stop" button
# Add a "Stop" time
# Add a "Stop after x times" feature
# Make the "Stop" time and "Stop after x times" options modifiable while the program is running.






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































