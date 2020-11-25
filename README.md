# Subreddit-Scraper

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/a2524ee0197c4c3e8377e8f01c3c4fde)](https://app.codacy.com/gh/Xenios91/Subreddit-Scraper?utm_source=github.com&utm_medium=referral&utm_content=Xenios91/Subreddit-Scraper&utm_campaign=Badge_Grade)

A simple web scraper for gathering data from subreddit's.

# CURRENTLY BEING WORKED ON
Details:

This initially worked using selenium to load Reddits dynamic pages, and it still does, however as time goes on if stb is very large, meaning you wish to grab more data, pages become too large to really work with and it causes chrome or firefox depending on the driver being used to become unstable due to the massive amounts of memory they take up and more page content for them to parse, this isn't a big deal on a modern desktop, however the goal of this project was to use raspberry pis to scrap data and their hardware constraints require an alternative method. To resolve this I will be changing how some of this works to not rely on chrome/firefox as much. A more static approach will be utilized to obtain subreddit data.
