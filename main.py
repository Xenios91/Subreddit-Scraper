import requests
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time

main_url = "https://www.reddit.com/r/politics/"


def get_webdriver() -> str:
    options = get_selenium_options()
    driver = webdriver.Firefox(
        options=options, executable_path=r'/home/xenios/repo/Web-Scraper/geckodriver')
    return driver


def get_selenium_options() -> Options:
    options = Options()
    #options.set_headless()
    return options


def get_html(driver: webdriver, url: str) -> str:
    driver.get(url)
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    html = driver.page_source
    return html


def main():
    driver = get_webdriver()
    response = get_html(driver, main_url)
    soup = BeautifulSoup(response, 'lxml')
    links = soup.findAll("article")
    for link in links:
        href = link.attrs.get("href")
        if "comments" in href:
            pass


main()
