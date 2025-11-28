import requests
import pandas as pd
from bs4 import BeautifulSoup

url = "https://news.ycombinator.com/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

span_titles = soup.find_all("span", class_="titleline")  # <-- updated class

data = []
for span in span_titles:
    a_tag = span.find("a")  # <-- find the <a> tag within the span
    data.append({"title": a_tag.text, "link": a_tag["href"]})
df = pd.DataFrame(data)
df.to_csv("hacker_news_titles.csv", index=False)


# Multiple pages
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://news.ycombinator.com/"
current_page_url = BASE_URL
headlines = []  # store the headlines here

for i in range(3):  # scrape first 3 pages
    response = requests.get(current_page_url)
    soup = BeautifulSoup(response.text, "html.parser")
    # extract headlines
    span_tags = soup.find_all("span", class_="titleline")
    for span in span_tags:
        a_tag = span.find("a")
        headlines.append({"title": a_tag.text, "link": a_tag["href"]})

    # find the link to the next page
    more_link = soup.find("a", class_="morelink")
    if more_link is None:
        break
    current_page_url = urljoin(BASE_URL, more_link["href"])

# save to CSV
print("Saving to csv...")
df = pd.DataFrame(headlines)
df.to_csv("hacker_news_multiple_pages.csv", index=False)
print("Done!")


#### A more flexible aprroach would be to keep going until no more "more" link is found. ####

from urllib.parse import urljoin
import requests
import pandas as pd
from bs4 import BeautifulSoup

BASE_URL = "https://news.ycombinator.com/"
headlines = []  # store the headlines here

start_page = int(input("Enter the start page number: "))  # eg 4
end_page = int(input("Enter the end page number: "))  # eg 8


# build the first URL dyanamically using the start page
current_url = f"{BASE_URL}news?p={start_page}"
current_page = start_page  # keep track of the current page


print(f"Scrapping from page {start_page} to {end_page}...")
# while loop with a limit
while current_url and current_page <= end_page:
    # request the page
    response = requests.get(current_url)
    soup = BeautifulSoup(response.text, "html.parser")

    # extract headlines
    span_tags = soup.find_all("span", class_="titleline")
    for span in span_tags:
        a_tag = span.find("a")
        headlines.append({"title": a_tag.text, "link": a_tag["href"]})

    # find the link to the next page
    more_link = soup.find("a", class_="morelink")
    if more_link:
        current_url = urljoin(BASE_URL, more_link["href"])
        current_page += 1  # increment the page count
    else:
        break  # no more pages


# save to CSV
print("Saving to csv...")
df = pd.DataFrame(headlines)
df.to_csv(f"hacker_news_pages_{start_page}_to_{end_page}.csv", index=False)
print(
    f"Scrapping completed from page {start_page} to {end_page}. Saved to hacker_news_multiple_pages.csv"
)
