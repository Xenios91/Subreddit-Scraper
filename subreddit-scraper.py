import os
from bs4 import BeautifulSoup
import time
import argparse
import requests

main_message = """
 _____       _                  _     _ _ _          _____
/  ___|     | |                | |   | (_) |        /  ___|
\ `--. _   _| |__  _ __ ___  __| | __| |_| |_ ______\ `--.  ___ _ __ __ _ _ __   ___ _ __
 `--. \ | | | '_ \| '__/ _ \/ _` |/ _` | | __|______|`--. \/ __| '__/ _` | '_ \ / _ \ '__|
/\__/ / |_| | |_) | | |  __/ (_| | (_| | | |_       /\__/ / (__| | | (_| | |_) |  __/ |
\____/ \__,_|_.__/|_|  \___|\__,_|\__,_|_|\__|      \____/ \___|_|  \__,_| .__/ \___|_|
                                                                         | |
                                                                         |_|
More info: https://github.com/Xenios91/Subreddit-Scraper
"""


def get_next_url(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    elements = soup.findAll("span", {"class": "next-button"})
    for element in elements:
        contents = element.contents[0]
        if "next" in contents.next:
            attrs = contents.attrs
            href = attrs.get("href")
            return href
    return "END"


def traverse_pages(url: str, page_count: int, file_name: str):
    traverse = True
    counter = 1
    while traverse:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            response = requests.get(url, headers=headers)
            html = response.text
            retrieve_all_post_urls(url, html, file_name)
            url = get_next_url(html)
            if url == "END":
                return
        except Exception as e:
            print(e)
        counter = counter + 1
        if counter > page_count and page_count != -1:
            traverse = False


def get_args() -> list:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-url", type=str, help="The subreddit to scrap. Example: -url https://www.reddit.com/r/ProgrammerHumor/", required=True)
    parser.add_argument(
        "-output", type=str, help="The filename to save the source to. Default is reddit_scrap_urls. Example: -output reddit_data", required=False, default="reddit_scrap_urls")
    parser.add_argument(
        "-pages", type=int, help="The number of pages to traverse, if -1 is used all pages will be traversed, the default is 10. Example -pages 200", required=False, default=10)
    args = parser.parse_args()
    return args


def retrieve_all_post_urls(url: str, html: str, file_name: str):
    file_name = "{0}{1}".format(file_name, "_urls")
    with open(file_name, "a") as file:
        soup = BeautifulSoup(html, 'lxml')
        links = soup.findAll("a", {"class": "comments"})
        for link in links:
            href = link.attrs.get("href")
            url_to_write = "{0}{1}".format(href, "\n")
            file.write(url_to_write)


def update_url(url: str) -> str:
    url = url.replace("www", "old")
    return url


def main():
    print(main_message)
    args = get_args()
    output_file = args.output
    url = args.url
    pages = args.pages

    try:
        url = update_url(args.url)
        print("Starting web scraping!")
        traverse_pages(url, pages, output_file)
        print("Done scraping {0}".format(url))
    except Exception:
        print("An error has occured")


main()
