#read in xlsx
import pandas as pd
import requests
from bs4 import BeautifulSoup
import concurrent.futures
import time

def get_real_url(first_url):
    data = requests.get(first_url).text
    # Creating BeautifulSoup object
    soup = BeautifulSoup(data, 'html.parser')
    # get all the tables (irrelevant now)
    tables = soup.find_all('table')
    # get the table  with the product list
    try:
        jeff = soup.find('table', class_='products-list').findAll('tr')[1]

        # find the first table, assume this is the product list
        # is this a valid assumption?
        #jeff= soup.findAll('table')[0].findAll('tr')[1]
        # get a list of links
        hrefs = jeff.find_all("a",href=True)
        # assume first one is the correct one
        # and only one link
        # here is the url we will actually use to find the secies
        link = hrefs[0]['href']
    except:
        return None
    #real_urls.append(link)
    return link
# this is used to time how long the script rns
# it ran for 15 minutes on my laptop
start_time = time.time()
# read in the excel file
xls = pd.ExcelFile('Pro Sci Recombinant Proteins SKU and Name Master File.xlsx')

# read the proteins sheet specifically
df1 = pd.read_excel(xls, 'proteins')
# grab column H 'vendor SKU'
vendor_sku = df1['Vendor SKU']

# loop over H
vendor_sku_list = vendor_sku.tolist()

#we don't have all the URLs to start with
#we have to figure that out,first by looking it up via SKU number
#then we can look for the real URL within that results page
urls=[]
#get list of urls
for sku in vendor_sku_list:
    url_name = "https://www.prosci-inc.com/catalogsearch/result/?q="+ str(sku)
    urls.append(url_name)

#this function looks up on the website simultaneously in parallel
#for all the URLs,that we determined,it executes the function get_real_url
real_urls=[]
with concurrent.futures.ThreadPoolExecutor() as executor:
    real_urls = executor.map(get_real_url, urls)

#we created text file to save the results of the real URLs were interested in
f = open("real urls.txt","w")
i =0
#for every URL that we found
for real_url in real_urls:
    #if there is any error at all,we just label it as invalid
    if real_url==None:
        f.write("Invalid\n")
    #if the results are legit,save it to the text file
    else:
        f.write(real_url+"\n")
#close the file
f.close()
# print out how long the script took to ran
e = int(time.time() - start_time)
print('{:02d}:{:02d}:{:02d}'.format(e // 3600, (e % 3600 // 60), e % 60))