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
# from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone
import os.path
from apscheduler.schedulers.blocking import BlockingScheduler
# from apscheduler.schedulers.background import BackgroundScheduler
import re
from urllib.request import Request, urlopen


# Function where everything we need to repeat goes.
def repeat_tasks():
    for u, p in zip(urls, page_titles):
        print(u, p)
        html = get_web_page(u)
        save_path = create_path(filename, save_here + p)
        print(save_path)
        store_copy(html, save_path)
    global copies_saved
    copies_saved += 1
    # Need a more graceful way to stop the scheduler; this throws an error
    if copies_saved == number_of_copies:
        scheduler.shutdown()



   
# Get the web page
def get_web_page(url_string):
    req = Request(url_string, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    mystr = webpage.decode("utf8")
    return mystr

    # Future functionality should get the suffix of the retrieved web page (.html, .htm, .cfm, etc.)
    # and then keep that to append to the end of the saved copy.

"""
old version:
    fp = urllib.request.urlopen(url_string)
    mybytes = fp.read()
    mystr = mybytes.decode("utf8")
    fp.close()
    return mystr
"""





def get_url_title(url_string):
    req = Request(url_string, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    title = str(webpage).split('<title>')[1].split('</title>')[0]
    return title[:40].strip()
    
"""
    webpage = urllib.request.urlopen(url_string).read()
    title = str(webpage).split('<title>')[1].split('</title>')[0]
    return title[:40].strip()
"""





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
    filename_w_time = filename_string + "-" + get_time_stamp()
    # Prepend the path
    return os.path.join(save_path, filename_w_time + ".html")     




# Function for storing the web site
# Got some of this code from: https://stackoverflow.com/questions/12517451/automatically-creating-directories-with-file-output
def store_copy(page_to_save, path_to_save_to):  
    os.makedirs(os.path.dirname(path_to_save_to), exist_ok=True)
    with open(path_to_save_to, "w") as file_obj:
        file_obj.write(page_to_save)  # this is what is being written to the file
    file_obj.close()


# Set what web pages to get
# Future functionality should ask what page to get, save a modifiable list of URLs
urls = [
        # GA 06: Lucy McBath vs Karen Handel - Needs updating
        "http://sos.ga.gov/index.php/elections/daily_turnout_reports_for_november_6_2018_election", 
        # TN Senate: Phil Bredesen vs Marsha Blackburn -  Might work
        "https://www.elections.tn.gov/county-results.php?OfficeByCounty=United%20States%20Senate", 
        # CA 49: Mike Levin vs. Diane Harkey - Needs updating
        "https://www.sos.ca.gov/elections/prior-elections/statewide-election-results/", 
        # CA 48: Harley Rouda vs. Dana Rohrabacker
        # CA 22: Andrew Jantz vs. Devin Nunes
        # CA 1: Audrey4congress vs. Doug LaMalfa
        # TX Senate: Beto O'Rourke vs. Ted Cruz - needs updating
        "https://www.sos.state.tx.us/elections/historical/index.shtml", 
        # OH 12: Danny O'Connor vs. Troy Balderson - needs updating
        "https://www.sos.state.oh.us/elections/election-results-and-data/2018-official-elections-results/", 
        # FL Senate: Bill Nelson vs. Gov. Rick Scott- needs updating
        "https://dos.myflorida.com/elections/data-statistics/elections-data/election-results-archive/",
        # WI 01: IronStache vs. Bryan Steill - needs updating
        "https://elections.wi.gov/elections-voting/results",
        # KS 03: Sharice Davids vs. Kevin Yoder - could work but would prefer a source link, this is local media
        "https://www.kwch.com/elections/?configID=1339"
        ]



"""
["http://example.com", 
        "http://www.behindthename.com/random/"]
"""
# ---- More elections we could add, non national, based on Jennifer Cohn's elections to watch: 
# Tony Evers vs. Scott Walker, WI governor
# Andrew Gillum vs. Ron DeSantis for FL governor
# Senator Laura Kelly vs. Kris Kobach for Kansas governor
# Stacey Abrams vs. Brian Kemp for GA governor
# Gretchen Whitmer vs. Bill Schuette for MI governor
# Rich Cordray vs. Mike DeWine for OH governor
# Kathleen Clyde vs. Frank LaRose for OH Sec of State

# Also would be good to add solid elections--ones not expected to be a surprise, either way.


# Initialize list for page titles, to be used as folder names to group downloaded results
page_titles = []
for x in urls:
    page_titles.append(re.sub("[\.\t\,\:;\(\)\.\|]", "", get_url_title(x), 0, 0))
    print(get_url_title(x))





# Set where to store the file/s, while ensuring directory/file name will 
# be compatible with Windows
save_here = 'C:/monitor/' 
# Future functionality should ask where to save to


# Set the retrieval frequency (in minutes) / how often 
# to retrieve a copy of the site
# Often I bump this down to 0.3 for testing, but probably should be at 5.0 for election day, assuming 144 collection times (set below)
frequency = 5.0
# Future functionality should ask the frequency


# Set how long the program will run for.
# Run the program this number of times / save this number of copies and then quit
number_of_copies = 144


# Initialize variable to keep track of how many times its run/how many copies saved
copies_saved = 0


# Establish what we'll call the saved version of the file
# Future functionality should just grab the web page title or other info and use that
# with remediation for duplicates (so if we've already grabbed a page titled 
# that, it'll add a version number or do some other remediation)
filename = "election_result"




# Repeat the retrieval according to the frequency chosen above
# code snippet originally from: https://stackoverflow.com/questions/22715086/scheduling-python-script-to-run-every-hour-accurately
# link to documentation: https://apscheduler.readthedocs.io/en/latest/ 
scheduler = BlockingScheduler()   
scheduler.add_job(repeat_tasks, 'interval', minutes = frequency)
scheduler.start()




### TO DO LIST ###
# Add more error handling to ensure we get the web page downloaded/copied

# Add functionality for capturing even more different URL suffixes/page types (html, pdf, etc.) 
# Add functionality for saving each file as its specific file type/suffix.

# Add functionality for dialog box GUI (goal is to make it easy for non-coders to use)

# Add functionality for building into an executable that can be run by non-coders

# Add a "Stop" button
# Add a "Stop" time
# Add a "Stop after x times" feature
# Make the "Stop" time and "Stop after x times" options modifiable while the program is running.

"""

# Testing ground
html = get_web_page("https://www.sos.state.oh.us/elections/election-results-and-data/2018-official-elections-results/")
                     https://www.sos.state.oh.us/elections/election-results-and-data/2018-official-elections-results/
print(html)
save_path = create_path(filename, save_here + get_url_title("https://www.sos.state.oh.us/elections/election-results-and-data/2018-official-elections-results/"))
print(save_path)
store_copy(html, save_path)




from urllib.request import Request, urlopen

req = Request('https://www.sos.state.oh.us/elections/election-results-and-data/2018-official-elections-results/', headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()
print(webpage)



"""




"""
Info for later, maybe

info and geturl

The response returned by urlopen (or the HTTPError instance) has two useful methods info() and geturl() and is defined in the module urllib.response..

geturl - this returns the real URL of the page fetched. This is useful because urlopen (or the opener object used) may have followed a redirect. The URL of the page fetched may not be the same as the URL requested.

info - this returns a dictionary-like object that describes the page fetched, particularly the headers sent by the server. It is currently an http.client.HTTPMessage instance.

Typical headers include ‘Content-length’, ‘Content-type’, and so on. See the Quick Reference to HTTP Headers for a useful listing of HTTP headers with brief explanations of their meaning and use.
"""























