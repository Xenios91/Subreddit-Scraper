import requests
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time

main_url = "https://www.reddit.com/r/politics/"
file_name = "reddit_politics.html"


def get_webdriver() -> str:
    options = get_selenium_options()
    driver = webdriver.Firefox(
        options=options, executable_path=r'/home/xenios/repo/Web-Scraper/geckodriver')
    return driver


def get_selenium_options() -> Options:
    options = Options()
    #options.set_headless()
    return options

def scroll_to_bottom(count: int, driver: webdriver):
    for _ in range(count):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

def get_html(driver: webdriver, url: str) -> str:
    driver.get(url)
    scroll_to_bottom(10, driver)
    html = driver.page_source
    return html

def write_to_file(data: str) -> bool:
    try:
        file = open(file_name, "w")
        file.write(data)
        file.close()
    except Exception as e:
        print(e)

def main():
    driver = get_webdriver()
    response = get_html(driver, main_url)
    soup = BeautifulSoup(response, 'lxml')
    soup = soup.prettify()
    success = write_to_file(soup)
    if success:
        print("Done scraping {0}".format(main_url))
    else:
        print("Scraping {0} failed".format(main_url))



main()
