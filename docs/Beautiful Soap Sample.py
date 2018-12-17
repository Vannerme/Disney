'''
Created on 10/12/2018

@author: jon
'''
import urllib2, sys
from bs4 import BeautifulSoup
import pandas as pd

# Identify the URL of the Website to scrape
site = "http://www.loc.gov/standards/iso639-2/php/code_list.php"

hdr = {'User-Agent': 'Mozilla/5.0'}
req = urllib2.Request(site,headers=hdr)
page = urllib2.urlopen(req)
soup = BeautifulSoup(page)
print soup

#Let's grab the column headers from the table. 
#In this case, the headers start in row 1 (hence limit 1)
column_headers = [th.getText() for th in 
                  soup.findAll('tr', limit=1)[0].findAll('th')]
print column_headers

#Now let's get the data to fill in the table. 
#The data is table format so a 2 dimensional list is needed. 
#Use 2: to skip the first row (headers)
data_rows = soup.findAll('tr')[2:]  

# now we have a list of table rows
print type(data_rows)  

#Now we combine the column_header list with the data_row list
lang_cd = [[td.getText() for td in data_rows[i].findAll(['td','th'])] for i in range(len(data_rows))] 

# Create an empty list to hold all the data
langcd_ls = [] 

# Now pass the list to the empty data frame
for i in range(len(data_rows)):  # for each table row
    code_row = []  # create an empty list for each pick/player

    # for each table data element from each table row
    for td in data_rows[i].findAll('td'):        
        # get the text content and append to the player_row 
        code_row.append(td.getText())        

    # then append each pick/player to the player_data matrix
    langcd_ls.append(code_row)

print lang_cd == langcd_ls

#Now we can create the data frame named df for the data extracted from the Website

lang_df = pd.DataFrame(lang_cd, columns=column_headers)

print lang_df.head(3)  # head() lets us see the 1st 3 rows of our DataFrame by default

# Finally, save the dataframe as a CSV
lang_df.to_csv('/home/jon/MLproject/data/LangCodes.csv', index=False)

