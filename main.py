import requests
from bs4 import BeautifulSoup

main_url = "https://www.reddit.com/r/politics/"

def get_html(url: str) -> str:
    response = requests.get(url).text
    return response

def main():
    response = get_html(main_url)
    soup = BeautifulSoup(response, 'lxml')
    links = soup.findAll("a")
    for link in links:
        href = link.attrs.get("href")
        if "comments" in href:
            pass

main()