from scraper import app
from scraper import reddit
from scraper.parser import parse_submission, parse_comment

'''
@app.task
def new_comment(comment_id):
    print('comment')  # reddit.comment(comment_id))


@app.task
def new_submission(submission_id):
    print('submission')  # reddit.submission(submission_id))


app.tasks.register(new_submission)
app.tasks.register(new_comment)
'''