###### -  This gives the loaded movies (25) since we have not used selenium here - ######


# scraping libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/117.0.0.0 Safari/537.36"
}
BASE_URL = "https://www.imdb.com/chart/top/"
response = requests.get(BASE_URL, headers=headers)

print(response.status_code)
soup = BeautifulSoup(response.text, "html.parser")

card = soup.find_all("li", class_="ipc-metadata-list-summary-item")


data = []
for item in card:
    id = item.find("div", class_="ipc-signpost__text").text
    title = item.find("h3", class_="ipc-title__text ipc-title__text--reduced").text
    year = item.find("span", class_="sc-b4f120f6-7 hoOxkw cli-title-metadata-item").text
    rating = item.find("span", class_="ipc-rating-star--rating").text
    votes = item.find("span", class_="ipc-rating-star--voteCount").text
    data.append(
        {
            "id": id,
            "title": title,
            "year": year,
            "rating": rating,
            "votes": votes,
        }
    )


def parse_votes(vote_str):
    vote_str = vote_str.replace("\xa0", "").strip(
        "() "
    )  # remove parentheses and spaces
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

df.to_csv("imdb_top_movies.csv", index=False)
print(df.head())
