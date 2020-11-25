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

# Maximum memory limit before the scraper saves and shuts down.
MEMORY_LIMIT = 90


def get_webdriver() -> str:
    print("Loading web driver", end="... ")
    options = get_selenium_options()
    driver_path = r"{}".format(os.getcwd() + "/geckodriver")
    driver = webdriver.Firefox(
        options=options, executable_path=driver_path)
    print("Web driver loaded!")
    return driver


def get_selenium_options() -> Options:
    options = Options()
    options.headless = True
    return options


def get_memory_stats() -> float:
    memory = psutil.virtual_memory()
    used_memory = memory.percent
    return used_memory


def scroll_to_bottom(count: int, driver: webdriver):
    percentage = 0.0
    for num in range(count):
        if num % 30 == 0:
            used_memory = get_memory_stats()
            if used_memory > MEMORY_LIMIT:
                print("{0} OF SYSTEM MEMORY UTILIZED".format(
                    used_memory), end="... ")
                print("RUNNING GC TO ATTEMPT TO FREE MEMORY")
                gc.collect()
                used_memory = get_memory_stats()
                if used_memory > MEMORY_LIMIT:
                    break
        try:        
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
        except Exception:
            #ignore script timeout
            pass
        percentage = (num/count) * 100
        print("Percent Complete: {0}%".format(round(percentage, 2)))


def get_html(driver: webdriver, url: str, stb: int) -> str:
    driver.get(url)
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, 'title')))
    except TimeoutException:
        print("PAGE TIMED OUT!")
        exit(1)
    scroll_to_bottom(stb, driver)
    html = driver.page_source
    return html


def write_to_file(data: str, file_name: str):
    try:
        print("Writing all scraped data to file", end="... ")
        file = open(file_name, "w")
        file.write(data)
        file.close()
        print("Data written!")
    except Exception as e:
        print(e)


def get_args() -> list:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-url", type=str, help="The subreddit to scrap. Example: -url news", required=True)
    parser.add_argument(
        "-output", type=str, help="The filename to save the source to. Default is reddit_scrap.html. Example: -output reddit_data", required=False)
    parser.add_argument(
        "-stb", type=int, help="The amount of times to scroll to the bottom of the subreddit to collect older results dynamically, the default is 75. Example -stb 200", required=False, default=75)
    args = parser.parse_args()
    return args


def retrieve_all_post_urls(file_name: str):
    print("Finding all post urls")
    with open(file_name, "r") as file:
        url_file_name = "{0}{1}".format(file_name, "_urls")
        url_file = open(url_file_name, "w")

        lines = "".join(file.readlines())
        soup = BeautifulSoup(lines, 'lxml')
        links = soup.findAll("a")
        percentage = 0.0
        amount_of_links = len(links)
        for counter, link in enumerate(links):
            url = link.attrs.get("href")
            if url and "https://www.reddit.com/r/politics/comments/" in url:
                url = "{0}{1}".format(url, "\n")
                url_file.write(url)
            percentage = (counter/amount_of_links) * 100
            print("Finding post {0}% complete".format(round(percentage, 2)))
    print("All post urls found!")


def main():
    print(main_message)
    args = get_args()
    driver = get_webdriver()
    try:
        print("Starting web scraping!")
        response = get_html(driver, args.url, args.stb)
        write_to_file(response, args.output)
        retrieve_all_post_urls(args.output)
        print("Done scraping {0}".format(args.url))
    except Exception:
        print("An error has occured")
    finally:
        #close all browser windows gracefully and end selenium
        driver.quit()


main()
