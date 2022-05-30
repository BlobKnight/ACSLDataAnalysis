import requests
import warnings
from bs4 import BeautifulSoup
import pandas as pd

warnings.simplefilter(action='ignore', category=FutureWarning) #Hiding FutureWarnings that Pandas throws
headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}


links = []
urls  = ["https://www.scores.acsl.org/leaderboard/teams/s3/","https://www.scores.acsl.org/leaderboard/teams/s5/"] #List of URLs to scrape
for url in urls: #Finding each team URL in both Senior sections to parse through
    tempLink = []
    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    for link in soup.findAll('a'):
        tempLink.append(link.get('href'))
    tempLink = tempLink[5:]
    links += tempLink


df = pd.DataFrame(columns=['Finals Shorts','Finals Programming','Total']) #Creating a dataframe to store the data

for link in links: #Parsing through each team's URL and storing the Finals Programming and Finals Shorts scores
     print(link)
     url = "https://www.scores.acsl.org/" + link
     html_content = requests.get(url).text
     soup = BeautifulSoup(html_content, 'html.parser')
     table = soup.find('table', class_='display compact')
     for row in table.tbody.find_all('tr'):
         # Find all data for each column
         columns = row.find_all('td')
         if (columns != []):
             prog = columns[19].text.strip()
             shorts = columns[17].text.strip()
             if shorts != '' and prog != '':
                df = df.append({'Finals Shorts': int(shorts), 'Finals Programming': int(prog), 'Total': int(int(shorts) + int(prog))},ignore_index=True)

medians=df.median() #Calculating the median of the dataframe
print(medians) #Printing the median


        






df.to_csv(r'C:\Users\shubh\Documents\ACSL2022\File Name.csv', index = False)
df = df[df['Finals Programming']!=0]
ax = df.plot.hist(column=["Finals Programming"],figsize=(20,10),range=[0, 20])
fig = ax.get_figure()
fig.savefig("prog.png")
df = df[df['Finals Shorts']!=0]
ax = df.plot.hist(column=["Finals Shorts"],figsize=(20,10),range = [0, 20])
fig = ax.get_figure()
fig.savefig("shorts.png")