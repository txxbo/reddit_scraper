from datetime import datetime


# parse submissions and comments
def parse_submission(submission) -> dict:
    author = submission.author
    name, karma, cake_day = parse_author(author)
    return {
        'title': submission.title,
        'author_id': name,
        'author_karma': int(karma),
        'author_cake_day': cake_day,
        'post_id': submission.id,
        'post_URL': submission.permalink,
        'body_image_URL': submission.url if submission.url.endswith((
            '.jpg', '.png', '.gif', '.jpeg')) else '',
        'body_text': submission.selftext,
        'timestamp':
            datetime.fromtimestamp(submission.created_utc).isoformat(),
        'vote': submission.score,
        'comment_count': submission.num_comments,
        'percent_upvoted': int(100 * submission.upvote_ratio),
        'subreddit': submission.subreddit.display_name,
        'comments': parse_comments(submission.comments),
    }


# parse all submissions and comments
def parse_all(submissions, submit=False) -> list:
    results = []
    for submission in submissions:
        post = parse_submission(submission)
        results.append(post)

    return results


# parse comments from a submission
def parse_comments(comments) -> list:
    results = []

    comments.replace_more(limit=None)
    for comment in comments.list():
        item = parse_comment(comment)
        results.append(item)

    return results


# parse single comment
def parse_comment(comment):
    name, karma, cake_day = parse_author(comment.author)
    item = {
        'comment_id': comment.id,
        'comment_body': comment.body,
        'vote': comment.score,
        'timestamp':
            datetime.fromtimestamp(comment.created_utc).isoformat(),
        'comment_author': name,
        'comment_author_karma': karma,
        'comment_author_cake_day': cake_day,
        'submission_id': comment.link_id,
        'parent_id': comment.parent_id,
    }

    return item


# def parse author
def parse_author(author) -> tuple:
    if author is None:
        return '', 0, ''

    name = author.name

    try:
        karma = author.comment_karma
    except:
        karma = 0

    try:
        cake_day = datetime.utcfromtimestamp(
            author.created_utc).strftime('%m-%d-%Y')
    except:
        cake_day = ''

    return name, karma, cake_day
