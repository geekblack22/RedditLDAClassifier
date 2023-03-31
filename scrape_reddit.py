from unittest import result
from bs4 import BeautifulSoup
import requests
URL = "http://redditlist.com/sfw"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
results = soup.find_all("div",class_="listing-item")
subreddits = []
for res in results:
    with open("subreddits.txt","w") as f:
        f.write( res["data-target-subreddit"])
   
    

# print(results)