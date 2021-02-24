import os
import praw
from celery import Celery
from dotenv import load_dotenv
from scraper.database import Database
from scraper.parser import parse_submission, parse_comment

load_dotenv()
config = {
    'client_id': os.getenv('client_id'),
    'client_secret': os.getenv('client_secret'),
    'user_agent': os.getenv('user_agent'),
    'parse_id': os.getenv('parse_id'),
    'parse_key': os.getenv('parse_key'),
    'database_url': os.getenv('database_url'),
    'redis_uri': os.getenv('redis_uri'),
}

reddit = praw.Reddit(
    client_id=config['client_id'],
    client_secret=config['client_secret'],
    user_agent=config['user_agent'])


def get_reddit():
    return reddit


app = Celery('tasks',
             broker=config['redis_uri'])
inspector = app.control.inspect()
db = Database(config)


@app.task
def new_comment(subreddit_name, comment_id):
    comment = reddit.comment(comment_id)
    item = parse_comment(comment)
    if db.post_comment(subreddit_name, comment.submission.id, item):
        # print(f"Wrote {item['comment_id']} to database")
        return True

    # print(f"C: Error:  {item['comment_id']} ")
    return False


@app.task
def new_submission(subreddit_name, submission_id):
    submission = reddit.submission(submission_id)
    item = parse_submission(submission)
    if db.post_submission(subreddit_name, item):
        # print(f"Wrote {item['post_id']} to database")
        return True

    # print(f"S: Error: {item['post_id']} ")
    return False
