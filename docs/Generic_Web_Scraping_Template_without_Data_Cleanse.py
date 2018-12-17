'''
Created on Mar 30, 2017

@author: jon
'''
import urllib2
from urllib2 import urlopen
from bs4 import BeautifulSoup
import pandas as pd

# Identify the URL of the Website to scrape
url = "http://www.basketball-reference.com/leagues/NBA_2014_per_game.html"

# This is the URL of the given Website
html = urlopen(url)

soup = BeautifulSoup(html,'lxml') 

print type(soup)

#Let's grab the column headers from the table. In this case, the headers start in row 2 (hence limit 2)

column_headers = [th.getText() for th in 
                  soup.findAll('tr', limit=1)[0].findAll('th')]

print column_headers

#Now let's get the data to fill in the table. The data is table format so a 2 dimensional list is needed.

data_rows = soup.findAll('tr')[1:]  # skip the first 2 header rows

print type(data_rows)  # now we have a list of table rows

player_data = [[td.getText() for td in data_rows[i].findAll(['td','th'])] for i in range(len(data_rows))] #I had to ammend the code here to include the TH tag


player_data_02 = []  # create an empty list to hold all the data

for i in range(len(data_rows)):  # for each table row
    player_row = []  # create an empty list for each pick/player

    # for each table data element from each table row
    for td in data_rows[i].findAll('td'):        
        # get the text content and append to the player_row 
        player_row.append(td.getText())        

    # then append each pick/player to the player_data matrix
    player_data_02.append(player_row)

print player_data == player_data_02

#Now we can create the data frame named df for the data extracted from the Website

df = pd.DataFrame(player_data, columns=column_headers)

print df.head(3)  # head() lets us see the 1st 3 rows of our DataFrame by default

#Now let's do some data cleansing to get the data in a better format. This may not always be neccesary

# Finding the None rows
#df[df['Pk'].isnull()]

#df = df[df.Player.notnull()]

#df[df['Pk'].isnull()]

#df.rename(columns={'WS/48':'WS_per_48'}, inplace=True)

# get the column names and replace all '%' with '_Perc'
#df.columns = df.columns.str.replace('%', '_Perc')

# Get the columns we want by slicing the list of column names
# and then replace them with the appended names
#df.columns.values[14:18] = [df.columns.values[14:18][col] + 
                                  #"_per_G" for col in range(4)]

#print(df.columns)

df.dtypes  # Take a look at data types in each column

df = df.convert_objects(convert_numeric=True)
df.dtypes

df = df[:].fillna(0) # index all the columns and fill in the 0s

#df.loc[:,'Yrs':'AST'] = df.loc[:,'Yrs':'AST'].astype(int)

print df.head() # All NaNs are now replaced with 0s

print df.dtypes # and we have the datatyps we want

#df.insert(0, 'Draft_Yr', 2014)  

#df.drop('Rk', axis='columns', inplace=True)

print df.columns # checkout our revised columns

#Now let's set up a template to extract the data for every year. We do that by simply creating a url template where we can change the year

url_template = "http://www.basketball-reference.com/leagues/NBA_{year}_per_game.html"

# create an empty DataFrame
draft_df = pd.DataFrame()

for year in range(1966, 2015):  # for each year
    url = url_template.format(year=year)  # get the url
    
    html = urlopen(url)  # get the html
    soup = BeautifulSoup(html, 'lxml') # create our BS object
    

    # get our player data
    data_rows = soup.findAll('tr')[1:] 
    player_data = [[td.getText() for td in data_rows[i].findAll(['td','th'])] for i in range(len(data_rows))]
    
    # Turn yearly data into a DataFrame
    year_df = pd.DataFrame(player_data, columns=column_headers)
    # create and insert the Draft_Yr column
    year_df.insert(0, 'Season_Yr', year)
    
    # Append to the big dataframe
    draft_df = draft_df.append(year_df, ignore_index=True)
    
print draft_df.head()

print draft_df.tail()

#Now again, let's clean up the data from all the years

# Convert data to proper data types
#draft_df = draft_df.convert_objects(convert_numeric=True)

# Get rid of the rows full of null values
#draft_df = draft_df[draft_df.Player.notnull()]

# Replace NaNs with 0s
#draft_df = draft_df.fillna(0)

# Rename Columns
#draft_df.rename(columns={'WS/48':'WS_per_48'}, inplace=True)
# Change % symbol
#draft_df.columns = draft_df.columns.str.replace('%', '_Perc')
# Add per_G to per game stats
#draft_df.columns.values[15:19] = [draft_df.columns.values[15:19][col] + 
 #                                 "_per_G" for col in range(4)]

# Changing the Data Types to int
#draft_df.loc[:,'Yrs':'AST'] = draft_df.loc[:,'Yrs':'AST'].astype(int)

# Delete the 'Rk' column
#draft_df.drop('Rk', axis='columns', inplace=True)

print draft_df.dtypes

#draft_df['Pk'] = draft_df['Pk'].astype(int) # change Pk to int

print draft_df.dtypes

print draft_df.isnull().sum() # No missing values in our DataFrame

#Finally, let's save the dataframe with all our data to a CSV file in our working directory (Eclipse Workspace)

draft_df.to_csv("seasonpergame_data_1966_to_2014.csv")

# sys allows us to get the info for the version of Python we use
import sys
import urllib2
import bs4

print('Python version:', sys.version_info)
print('Urllib.request version:', urllib2.__version__)
print('BeautifulSoup version:', bs4.__version__)
print('Pandas version:', pd.__version__)












