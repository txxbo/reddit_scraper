import time
from psaw import PushshiftAPI
from datetime import datetime, timedelta
from scraper import db, get_reddit, new_submission


def collect():
    print(f'* Downloading subreddits from server')
    subreddits = db.get_subreddits()

    print(f'* Collecting threads from Reddit API')
    submissions = []

    initial = time.time()
    while True:
        current_date, next_date = get_dates()

        if next_date > datetime.utcnow():
            next_date = datetime.utcnow()

        if current_date >= datetime.utcnow() - timedelta(hours=1):
            break

        for subreddit in subreddits:
            submissions = []
            print(f"Grabbing {current_date} to {next_date} for {subreddit['name']}")
            try:
                data = get_submissions_by_date_range(subreddit, current_date, next_date,)
                submissions.extend(data)
                print(f"Received {len(data)} submissions")
            except:
                print(f"Error, bad response. Written to errors.txt")
                with open('errors.txt', 'a') as f:
                    f.write(f"PSAPIErr: {current_date} to {next_date} for {subreddit['name']}\n")

            for submission in submissions:
                new_submission.delay(subreddit['name'], submission.id)

        write_date(next_date)

    final = time.time()
    print(f"Time: {round(final-initial, 1)} seconds")
    # print(f"Posts found: {len(submissions)}")


def write_date(d):
    result = d
    with open('next_time.txt', 'w') as f:
        f.write(str(int(result.timestamp())))


def get_dates(delta=60*4):
    with open('next_time.txt', 'r') as f:
        d = datetime.fromtimestamp(int(f.read().strip()))
        next_date = d+timedelta(minutes=delta)
        return d, next_date


# get submissions from subreddits
def get_submissions(sub, mode='new', limit=3, time_filter='all') -> list:
    reddit = get_reddit()
    subreddit = reddit.subreddit(sub['name'])

    if mode == 'top':
        return subreddit.top(time_filter=time_filter, limit=limit)
    elif mode == 'hot':
        return subreddit.hot(limit=limit)
    return subreddit.new(limit=limit)


# get submissions from subreddits in date range
def get_submissions_by_date_range(subreddit,
                                  first_date,
                                  second_date,
                                  limit=None) -> list:
    reddit = get_reddit()
    api = PushshiftAPI(reddit)
    after_epoch = int(first_date.timestamp())
    before_epoch = int(second_date.timestamp())
    return list(api.search_submissions(after=after_epoch,
                                       before=before_epoch,
                                       subreddit=subreddit['name'],
                                       limit=None
                                       ))


if __name__ == '__main__':
    collect()
