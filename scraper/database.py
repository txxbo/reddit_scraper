from urllib.parse import urlencode
import requests
import json


# get list of subreddits from parse server api
class Database:
    def __init__(self, config):
        self.config = config
        self.url = config['database_url']

    def get_subreddits(self) -> list:
        headers = self.get_headers()
        res = requests.get(url=f'{self.url}subreddits', headers=headers)

        if res.status_code == 200:
            return json.loads(res.text)['results']
        else:
            return []

    # get headers for parse server api
    def get_headers(self) -> dict:
        return {
            'X-Parse-Application-Id': self.config['parse_id'],
            'X-Parse-REST-API-Key': self.config['parse_key']
        }

    # send back to nodechef
    def post_submission(self, subreddit, submission) -> bool:
        response = requests.post(url=f'{self.url}{subreddit}',
                                 headers=self.get_headers(),
                                 json=submission)

        if not response.status_code == 201:
            print(response.status_code, response.text)

        return response.status_code == 201

    def post_comment(self, subreddit, submission_id, comment):
        query = {
            "comments": {
                "__op": "AddUnique",
                "objects": [comment],
            }
        }
        object_id = self.find_submission(subreddit, submission_id)

        response = requests.put(f"{self.url}{subreddit}/{object_id}",
                                headers=self.get_headers(),
                                json=query)

        # if submission isn't in database yet, it will
        # give 404 error. should we add it if not found?
        # or let script continue?
        return response.status_code == 200

    def find_submission(self, subreddit, submission_id):
        params = urlencode({"where": json.dumps({"post_id": submission_id})})
        response = requests.get(f"{self.url}{subreddit}?{params}",
                                headers=self.get_headers())

        data = response.json()['results']
        if len(data) >= 1:
            return data[0]['objectId']
        return ''
