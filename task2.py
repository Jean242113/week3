import requests
from bs4 import BeautifulSoup
import csv


def create_csv(file_name, datas):
    with open(file_name, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        for data in datas:
            writer.writerow(data)


def Search(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    result = []
    articleTitle = soup.select(".r-ent")
    for title in articleTitle:
        # print(title)
        if title.select_one(".title a"):
            Count = (
                title.select_one("span").getText() if title.select_one("span") else "0"
            )
            textTitle = (
                title.select_one(".title a").getText()
                if title.select(".title a")
                else ""
            )

            article_response = requests.get(
                "https://www.ptt.cc" + title.select_one(".title a")["href"]
            )
            article_soup = BeautifulSoup(article_response.text, "html.parser")
            metadata = article_soup.find_all("span", class_="article-meta-value")
            if len(metadata) >= 4:
                post_time = metadata[3].text
                result.append([textTitle, Count, post_time])
            else:
                result.append([textTitle, Count])
    prev_page = soup.select_one(".btn-group-paging a:nth-of-type(2)")
    prev_url = f"https://www.ptt.cc{prev_page['href']}" if prev_page else None
    return result, prev_url


if __name__ == "__main__":
    datas, prev_url = Search("https://www.ptt.cc/bbs/Lottery/index.html")
    temp, prev_url = Search(prev_url)
    datas.extend(temp)
    temp, prev_url = Search(prev_url)
    datas.extend(temp)
    create_csv("article.csv", datas)
