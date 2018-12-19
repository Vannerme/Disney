## Project to Screen Scrape Disney Wait Times from Website
## Source: https://www.parkgeni.us/disney-world/magic-kingdom/its-a-small-world/wait-times/2018-12-16

# import libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

#Create two empty lists to store the wait time and the ride names
ride_data=[]
name_data=[]
  
# Identify the URL and substitue %s for the looped url name
url_template = "https://www.parkgeni.us/disney-world/magic-kingdom/%s/wait-times/2018-12-18"


# Create the list of URLs to imput into loop
ride=["its-a-small-world","astro-orbiter","big-thunder-mountain-railroad","buzz-lightyears-space-ranger-spin","dumbo-the-flying-elephant","haunted-mansion","jungle-cruise","monsters-inc-laugh-floor","peter-pans-flight","pirates-of-the-caribbean","seven-dwarfs-mine-train","space-mountain","splash-mountain","stitchs-great-escape","the-barnstomer","the-many-adventures-of-winnie-the-pooh","tomorrowland-speedway","tomorrowland-transist-authority-people-mover","walt-disneys-carousel-of-progress"]

# Create the loop to run each URL and create the soup object
for i in ride:  #name for each ride
    url = url_template %i  # get the url
    
    print url
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

# Search the returned HTML and extract the wait times
    all_scripts = soup.find_all('script')
    parse=(all_scripts[1].text)
    parse = parse[33:]
    x=re.findall(r'waitTime"(.*?)},',parse)
    rows = re.findall(r'waitTime":(.*?)},',parse)
    
# Append all wait times as elements of a list
    ride_data.append(rows)

# Append all ride names as elements of a lsit
    name_data.append(url)   

# Create a dataframe from the lists of waittimes and rides    
df=pd.DataFrame({"WaitTime":ride_data,"Name":name_data})

# Flatten out the wait time column and apply ride name to each wait time value    
df=df.set_index(['Name']).WaitTime.apply(pd.Series).stack().reset_index(['Name'], name='WaitTime')

# Save the final results to CSV
df.to_csv('/Disney/data/ridesOutput.csv')



  





