import praw
import pandas


class SubredditURLScraper():
    reddit = None
    post_list = []

    def __init__(self, client_id, client_secret):
        # [Being used to pass client_id and client_secret to the object for using PRAW.]

        # Args:
        #    client_id ([str]): [Your client id supplied by Reddit.]
        #    client_secret ([str]): [Your client secret supplied by Reddit.]

        self.reddit = praw.Reddit(client_id=client_id, client_secret=client_secret,
                                  user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36')
        self.reddit.read_only = True

    def scrap_subreddit(self, subreddit: str, limit: int) -> pandas.DataFrame:
        if limit == -1:
            posts = self.reddit.subreddit(subreddit).new(limit=None)
        else:
            posts = self.reddit.subreddit(subreddit).new(limit=limit)

        counter = 0
        for post in posts:
            self.post_list.append([post.title, post.subreddit, post.permalink,
                                   post.url, post.num_comments, post.selftext])
            counter = counter + 1
        data = pandas.DataFrame(
            self.post_list, columns=['title', 'subreddit', 'reddit_post_url', 'article_linked', 'num_comments', 'body'])
        print("{0} post have been collected from the {1}".format(
            counter, subreddit))
        return data


class PostCommentScraper():
    comments = []


class DataFrameUtils():

    @staticmethod
    def write_csv_to_file(file_name: str, sep: str, dataframe: pandas.DataFrame):
        try:
            dataframe.to_csv(file_name, sep=sep)
            print("Wrote {0} values from dataframe to file [{1}]".format(
                dataframe.shape[0], file_name))
        except Exception as e:
            print(e)
