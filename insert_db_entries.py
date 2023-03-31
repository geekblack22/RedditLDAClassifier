import os
import time
from unittest import result
from bs4 import BeautifulSoup
import requests

def main():
    URL = "http://redditlist.com/sfw"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find_all("div",class_="listing-item")
    subreddits = []
    for res in results:
        subreddits.append(res["data-target-subreddit"])
    i = 0
    while(True):
        try:
            print("STARTING DATA TRANSFER")
            os.system("python load_voice.py "+subreddits[i])
            i+= 1
        except:
            print("HERE WE GO AGAIN!!!")              
            time.sleep(300)
            i+= 1
        

if __name__ == "__main__":
    main()
