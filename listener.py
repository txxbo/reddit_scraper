import time
from scraper import new_submission, new_comment, db, get_reddit, tickers


def listener():
    subreddit_list = db.get_subreddits()
    reddit = get_reddit()

    subreddits = [reddit.subreddit(sub['name'])
                  for sub in subreddit_list]

    print(f"Subreddits: {', '.join([sub.display_name for sub in subreddits])}")

    comments = {}
    submissions = {}
    for subreddit in subreddits:
        comments[subreddit] = subreddit.stream.comments(pause_after=-1)
        submissions[subreddit] = subreddit.stream.submissions(pause_after=-1)

    while True:
        for subreddit in comments:
            for comment in comments[subreddit]:
                if comment is not None:
                    new_comment.delay(subreddit.display_name, comment.id)
                else:
                    break
            for submission in submissions[subreddit]:
                if submission is not None:
                    new_submission.delay(subreddit.display_name, submission.id)
                else:
                    break
            time.sleep(1)


if __name__ == "__main__":
    if len(tickers) > 0:
        print('Listening...')
        listener()
    else:
        print(f"No tickers found.")
