### --- THis loads all the 250 movies using selenium  and saves it to a CSV --- ###

# selenium to login to a website and scrape data
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# scraping libraries
from bs4 import BeautifulSoup
import pandas as pd

# chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in the background
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/117.0.0.0 Safari/537.36"
)


# Path to your ChromeDriver
service = Service("C:/Users/dante/Downloads/chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)


BASE_URL = "https://www.imdb.com/chart/top/"
driver.get(BASE_URL)
time.sleep(2)  # wait for page to fully load JS


print(driver.page_source[:5000])  # print first 5000 chars of HTML

# parse with beautifulsoup
soup = BeautifulSoup(driver.page_source, "html.parser")

# select all movie cards

cards = soup.find_all("li", class_="ipc-metadata-list-summary-item")
print("Number of movies found:", len(cards))  # should be 250


# extract data
data = []
for item in cards:
    id = item.find("div", class_="ipc-signpost__text").text
    title = item.find("h3", class_="ipc-title__text ipc-title__text--reduced").text
    year = item.find("span", class_="sc-b4f120f6-7 hoOxkw cli-title-metadata-item").text
    rating = item.find("span", class_="ipc-rating-star--rating").text
    votes = item.find("span", class_="ipc-rating-star--voteCount").text

    data.append(
        {"id": id, "title": title, "year": year, "rating": rating, "votes": votes}
    )


# clean and save
def parse_votes(vote_str):
    vote_str = vote_str.replace("\xa0", "").strip("() ")
    if "M" in vote_str:
        return int(float(vote_str.replace("M", "")) * 1_000_000)
    elif "K" in vote_str:
        return int(float(vote_str.replace("K", "")) * 1_000)
    else:
        return int(vote_str.replace(",", ""))


df = pd.DataFrame(data)
df["votes"] = df["votes"].apply(parse_votes)
df["rating"] = df["rating"].astype(float)
df["year"] = df["year"].str.strip("()").astype(int)

df.to_csv("imdb_top_250.csv", index=False)
print(df.head())
driver.quit()  # close browser
print("Data saved to imdb_top_250.csv")
