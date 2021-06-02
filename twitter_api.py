from urllib.parse import urljoin
import urllib3
from config import config
import json
import util


class TwitterApi:
    _stream_url = urljoin(config.twitter.url, '/2/tweets/search/stream/')

    _auth_header = {'Authorization': f'Bearer {config.twitter.token}'}

    _http = urllib3.PoolManager()

    def _retweet_url(self, tweetId):
        return urljoin(config.twitter.url, f'/1.1/statuses/retweet/{tweetId}.json')

    def _stream_filter(self, user_ids):
        filter_str = ' '.join([f'from:{user}' for user in user_ids])
        return {'add': [{'value': filter_str}]}

    def _check_if_success(self, response):
        if response.status < 200 or response.status >= 300:
            raise Exception(f'HTTP {response.status} response')

    def stream(self, user_ids):
        body = json.dumps(self._stream_filter(user_ids))
        r = self._http.request('POST', self._stream_url, body=body, headers=self._auth_header)
        self._check_if_success(r)
        for tweet in util.read_json_stream(r):
            if not hasattr(tweet, "in_reply_to_status_id"):
                # Dont forward replies
                yield tweet

    def retweet(self, tweetId):
        r = self._http.request('POST', self._retweet_url(tweetId), headers=self._auth_header)
        self._check_if_success(r)
        return json.load(r)
