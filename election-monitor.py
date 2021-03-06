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
#from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone
import os.path
from apscheduler.schedulers.blocking import BlockingScheduler
# from apscheduler.schedulers.background import BackgroundScheduler
import re
from urllib.request import Request, urlopen
#import urllib.request
import io



# Set what web pages to get
# Future functionality should ask what page to get, save a modifiable list of URLs
urls = [
        # LOOKS GOOD PRE-VOTING -  TN Senate: Phil Bredesen vs Marsha Blackburn -  Might work
        "https://www.elections.tn.gov/county-results.php?OfficeByCounty=United%20States%20Senate", 
        # LOOKS GOOD PRE-VOTING -  TX Senate: Beto O'Rourke vs. Ted Cruz - needs updating
        "https://enrpages.sos.state.tx.us/public/nov06_331_race0.htm", 
        # LOOKS GOOD PRE-VOTING -  KS 03: Sharice Davids vs. Kevin Yoder - could work but would prefer a source link, this is local media
        "https://www.kwch.com/elections/?configID=1339",
        # LOOKS GOOD PRE-VOTING -  UT Senate: Jenny Wilson vs. Mitt Romney 
        "https://electionresults.utah.gov/elections/federal",
        # LOOKS GOOD PRE-VOTING -  MI 4th: John Moolenaar (R) vs. Jerry Hilliard (D) 
        "https://mielections.us/election/results/2018GEN_CENR.html",
        # LOOKS GOOD PRE-VOTING - OR 1st: Suzanne Bonamici vs. John Verbeek vs. Drew Layda
        "http://results.oregonvotes.gov/resultsSW.aspx?type=FED&map=CTY",
        # LOOKS GOOD PRE-VOTING - NM Senate: Martin Heinrich vs. Mick Rich vs. Gary Johnson
        "http://electionresults.sos.state.nm.us/resultsSW.aspx?type=FED&map=CTY",
        # LOOKS GOOD PRE-VOTING - WA Senate: Maria Cantwell vs. Susan Hutchinson 
        "https://results.vote.wa.gov/results/current/US-Senator_ByCounty.html",

        # FL Senate: Bill Nelson vs. Gov. Rick Scott- needs updating after 5pm
        "https://floridaelectionwatch.gov/ContestResultsByCounty/120000",
        # WI 01: IronStache vs. Bryan Steill - Unfortunately they post unofficial results by county. Sheeshers. Waukesha county
        "https://electionresults.waukeshacounty.gov/contests.aspx?contest=5",
        # WI 01: IronStache vs. Bryan Steill - Unfortunately they post unofficial results by county. Sheeshers. Milwaukee county
   #     "https://county.milwaukee.gov/files/county/county-clerk/Election-Commission/ElectionResultsCopy-1/2018Copy-1/11-2-18FallGeneralElection-WardbyWard-UnofficialResults.txt"
        # CA 49: Mike Levin vs. Diane Harkey - Needs updating at 8pm
        "https://vote.sos.ca.gov/returns/us-rep/district/49",
        # CA 48: Harley Rouda vs. Dana Rohrabacker
        "https://vote.sos.ca.gov/returns/us-rep/district/48",
        # CA 22: Andrew Jantz vs. Devin Nunes
        "https://vote.sos.ca.gov/returns/us-rep/district/22",
        # CA 1: Audrey4congress vs. Doug LaMalfa
        "https://vote.sos.ca.gov/returns/us-rep/district/1"
        # GA Governor Abrams    <--- throws list index out of range error
  #      "https://results.enr.clarityelections.com/GA/Colquitt/91675/216647/reports/detailxml.zip"
        # GA 06: Lucy McBath vs Karen Handel - Coming in blank
  #      "https://results.enr.clarityelections.com/GA/91639/Web02-state.216038/#/c/C_2"

        
        # ALSO TRACKING THE FOLLOWING 'SURE THING'S':

        # NY 26th: Brian Higgins (D) vs. Renee Zeno       Causing error, but otherwise looks ready
  #      "http://www.elections.ny.gov/ENR/NYSENRAccessible.html",
        # CT 3rd: Rosa L. DeLauro (D) vs. Angel Cadena
   #     "https://ctemspublic.pcctg.net/#/home"
            # "https://portal.ct.gov/SOTS/Election-Services/Election-Results/Election-Results",
        # MS Senate: David Baria (D) vs. Roger F. Wicker (R)
   #     "http://www.sos.ms.gov/Elections-Voting/Pages/2018-Elections-Results.aspx",   
        
        # Adding NYTimes House Tracker    <--- throwing list index out of range error
  #      "https://www.nytimes.com/interactive/2018/11/06/us/elections/results-house-elections.html"
        
        # Adding NYTimes Senate Tracker     <--- throwing list index out of range error
  #      "https://www.nytimes.com/interactive/2018/11/06/us/elections/results-senate-elections.html",
  
        # OH 12: Danny O'Connor vs. Troy Balderson - total dyanmic page, bleh.
  #      "https://www.sos.state.oh.us/"  
        # PA 9th: Dan Meuser (R) vs. Denny Wolff  ----dynamically generated page: https://stackoverflow.com/questions/8960288/get-page-generated-with-javascript-in-python
  #      "https://www.electionreturns.pa.gov/General/CountyBreakDownResults?officeId=2&districtId=1&ElectionID=63&ElectionType=G&IsActive=1",
        # NC 11th: Mark Meadows vs. Phillip G. Price vs. Clifton Ingram Jr.    <---- d
   #     "https://er.ncsbe.gov/contest_details.html?election_dt=11/06/2018&county_id=0&contest_id=1185",
        ]


# ---- More elections we could add, non national, based on Jennifer Cohn's elections to watch: 
# Tony Evers vs. Scott Walker, WI governor
# Andrew Gillum vs. Ron DeSantis for FL governor
# Senator Laura Kelly vs. Kris Kobach for Kansas governor
# Stacey Abrams vs. Brian Kemp for GA governor
# Gretchen Whitmer vs. Bill Schuette for MI governor
# Rich Cordray vs. Mike DeWine for OH governor
# Kathleen Clyde vs. Frank LaRose for OH Sec of State

# Also would be good to add solid elections--ones not expected to be a surprise, either way.





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
number_of_copies = 100


# Initialize variable to keep track of how many times its run/how many copies saved
copies_saved = 0


# Establish what we'll call the saved version of the file
# Future functionality should just grab the web page title or other info and use that
# with remediation for duplicates (so if we've already grabbed a page titled 
# that, it'll add a version number or do some other remediation)
filename = "election_result"






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
    
    #get = urllib.request.urlopen(url_string)
    #webpage = get.read()
    #soup = BeautifulSoup(webpage, "lxml")
    #return str(soup.encode("utf-8"))
    
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
    with io.open(path_to_save_to, "w", encoding="utf-8") as file_obj:
    
    #with open(path_to_save_to, "w") as file_obj:
        file_obj.write(page_to_save)  # this is what is being written to the file
    file_obj.close()




# Initialize list for page titles, to be used as folder names to group downloaded results
page_titles = []
page_order = 1
for x in urls:
    page_titles.append(re.sub('[^a-zA-Z0-9 \n\.]', '', str(page_order) + " " + get_url_title(x), 0, 0))
    page_order += 1
    # page_titles.append(re.sub("[\.\t\,\:;\(\)\.\|]", "", get_url_title(x), 0, 0))
    print(page_titles[-1])



# Run the regular tasks once, before we start the timed runs.
repeat_tasks()


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























