import argparse
import subreddit_utils

main_logo = '''
   _____       _                  _     _ _ _          _____                                
  / ____|     | |                | |   | (_) |        / ____|                               
 | (___  _   _| |__  _ __ ___  __| | __| |_| |_ _____| (___   ___ _ __ __ _ _ __   ___ _ __ 
  \___ \| | | | '_ \| '__/ _ \/ _` |/ _` | | __|______\___ \ / __| '__/ _` | '_ \ / _ \ '__|
  ____) | |_| | |_) | | |  __/ (_| | (_| | | |_       ____) | (__| | | (_| | |_) |  __/ |   
 |_____/ \__,_|_.__/|_|  \___|\__,_|\__,_|_|\__|     |_____/ \___|_|  \__,_| .__/ \___|_|   
                                                                           | |              
More info: https://github.com/Xenios91/Subreddit-Scraper                                                                        |_|              
'''

def get_args() -> list:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--subreddit", type=str, help="The subreddit to scrap. Example: --subreddit ProgrammerHumor", required=True)
    parser.add_argument(
        "--output", type=str, help="The filename to save the source to. Default is reddit_[subreddit]_urls. Example: --output reddit_data", required=False, default="reddit_[subreddit]_urls")
    parser.add_argument(
        "--cid", type=str, help="Your client ID. Example: --cid=47djfhshg3756j", required=True)
    parser.add_argument(
        "--cs", type=str, help="Your client secret. Example: --cs=nvb67462nfFF58221fzaa", required=True)
    parser.add_argument(
        "--limit", type=int, help="The amount of post you want to scrap, if -1 is used it will pull all data available. Example: --limit 100. The Default is 10", required=False, default=10)
    args = parser.parse_args()
    return args

def change_file_name(filename: str, subreddit: str) -> str:
    if "[subreddit]" in filename:
        filename = filename.replace("[subreddit]", subreddit)
    return filename

def main():
    args = get_args()
    file_name = change_file_name(args.output, args.subreddit)
    reddit_url_scraper = subreddit_utils.SubredditURLScraper(
        args.cid, args.cs)
    dataframe = reddit_url_scraper.scrap_subreddit(args.subreddit, args.limit)
    subreddit_utils.DataFrameUtils.write_csv_to_file(
        file_name, ",", dataframe)


main()
