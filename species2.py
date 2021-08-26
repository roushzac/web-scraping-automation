import pandas as pd
import requests
from bs4 import BeautifulSoup
import concurrent.futures
import time
# record this to see how long it took
start_time = time.time()
# read in list of urls from files
f = open("real urls.txt","r")
urls=[]
for line in f:
    urls.append(line.strip())
f.close()


urls2=urls
# this function grabs the species name off the website
def get_species(url):
    if url=='Invalid':
        return 'Invalid'
    data = requests.get(url).text
    # Creating BeautifulSoup object
    soup = BeautifulSoup(data, 'html.parser')
    # get all the tables (irrelevant now)
    #tables = soup.find_all('table')
    #df = pd.DataFrame(urls)
    #jeff = soup.find('table', class_='prop-table')
    rows=list()
    for caption in soup.find_all('caption'):
        if caption.get_text() == 'Specifications':
            table = caption.find_parent('table', {'class': 'prop-table'})

            for row in table.findAll("tr"):
                rows.append(row)
    species = rows[0].text
    species= species.split('SPECIES:')[1]
    return species

# this runs the function get_species on all the urls in urls2 in parallel
# this basically means that we are grabbing the species name from each website simultaneously,
# or all at the same time
with concurrent.futures.ThreadPoolExecutor() as executor:
    results = executor.map(get_species, urls2)

species_list=[]
# for every species name we found in results
for species_name in results:
    # label invalid if it was invalid
    if species_name=='Invalid':
        species_list.append('Invalid')
    # otherwise record the species name
    else:
        species_list.append(species_name)


# convert the list of species into a datframe
df = pd.DataFrame(species_list)
# save that to an excel sheeet
df.to_excel("automated species.xlsx")

# print out how long it took
# took me 10 minutes
e = int(time.time() - start_time)
print('{:02d}:{:02d}:{:02d}'.format(e // 3600, (e % 3600 // 60), e % 60))