import requests
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import argparse
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import psutil
import gc

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


# File extension to save all output as.
FILE_EXTENSION = ".html"
# Maximum memory limit before the scraper saves and shuts down.
MEMORY_LIMIT = 90


def get_webdriver() -> str:
    options = get_selenium_options()
    driver = webdriver.Firefox(
        options=options, executable_path=r'/home/xenios/repo/Web-Scraper/geckodriver')
    return driver


def get_selenium_options() -> Options:
    options = Options()
    options.set_headless()
    return options


def get_memory_stats() -> float:
    memory = psutil.virtual_memory()
    used_memory = memory.percent
    return used_memory


def scroll_to_bottom(count: int, driver: webdriver):
    for num in range(count):
        if num % 2 == 0:
            used_memory = get_memory_stats()
            if used_memory > MEMORY_LIMIT:
                print("RUNNING GC TO ATTEMPT TO FREE MEMORY")
                gc.collect()
                used_memory = get_memory_stats()
                if used_memory > MEMORY_LIMIT:
                    break
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)


def get_html(driver: webdriver, url: str, stb: int) -> str:
    driver.get(url)
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, 'title')))
    except TimeoutException:
        print("PAGE TIMED OUT!")
        exit(1)
    scroll_to_bottom(10, driver)
    html = driver.page_source
    return html


def write_to_file(data: str, file_name: str) -> bool:
    if not file_name.endswith(FILE_EXTENSION):
        file_name = file_name.split('.')
        end = len(file_name)
        if end > 1:
            file_name[end - 1] = FILE_EXTENSION
        else:
            file_name = "".join(file_name) + FILE_EXTENSION
        file_name = "".join(file_name)
    try:
        file = open(file_name, "w")
        file.write(data)
        file.close()
        return True
    except Exception as e:
        print(e)
        return False


def get_args() -> list:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-url", type=str, help="The subreddit to scrap. Example: -url news", required=True)
    parser.add_argument(
        "-output", type=str, help="The filename to save the source to. Default is reddit_scrap.html. Example: -output reddit_data.html", required=False)
    parser.add_argument(
        "-stb", type=int, help="The amount of times to scroll to the bottom of the subreddit to collect older results dynamically, the default is 10. Example -stb 100", required=False, default=10)
    args = parser.parse_args()
    return args


def main():

    args = get_args()
    driver = get_webdriver()
    response = get_html(driver, args.url, args.stb)
    soup = BeautifulSoup(response, 'lxml')
    soup = soup.prettify()
    success = write_to_file(soup, args.output)
    if success:
        print("Done scraping {0}".format(args.url))
    else:
        print("Scraping {0} failed".format(args.url))


main()
