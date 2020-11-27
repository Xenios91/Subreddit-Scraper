import argparse
import subreddit_utils


def get_args() -> list:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--subreddit", type=str, help="The subreddit to scrap. Example: --subreddit ProgrammerHumor", required=True)
    parser.add_argument(
        "--output", type=str, help="The filename to save the source to. Default is reddit_scrap_urls. Example: --output reddit_data", required=False, default="reddit_scrap_urls")
    parser.add_argument(
        "--cid", type=str, help="Your client ID. Example: --cid=47djfhshg3756j", required=True)
    parser.add_argument(
        "--cs", type=str, help="Your client secret. Example: --cs=nvb67462nfFF58221fzaa", required=True)
    parser.add_argument(
        "--limit", type=int, help="The amount of post you want to scrap, if -1 is used it will pull all data available. Example: --limit 100. The Default is 10", required=False, default=10)
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    reddit_url_scraper = subreddit_utils.SubredditURLScraper(
        args.cid, args.cs)
    dataframe = reddit_url_scraper.scrap_subreddit(args.subreddit, args.limit)
    subreddit_utils.DataFrameUtils.write_csv_to_file(
        args.output, ",", dataframe)


main()
