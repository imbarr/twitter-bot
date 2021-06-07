from urllib.parse import urljoin, urlencode
from requests_oauthlib import OAuth1Session, OAuth2Session
import config


class TwitterApi:
    _url = config.get_config()["twitter"]["url"]
    _cfg = config.get_config()["twitter"]

    def _get_oauth1_session(self):
        return OAuth1Session(
            client_key=self._cfg["api_key"],
            client_secret=self._cfg["api_secret"],
            resource_owner_key=self._cfg["access_token"],
            resource_owner_secret=self._cfg["access_secret"]
        )

    def _get_oauth2_session(self):
        return OAuth2Session(
            token={
                'token_type': 'Bearer',
                'access_token': self._cfg["bearer_token"]
            }
        )

    def _retweet_url(self, tweet_id):
        return urljoin(self._url, f'/1.1/statuses/retweet/{tweet_id}.json')

    def _fetch_url(self, since_time, since_id, users):
        filters = ' '.join([f"from: {user}" for user in users])
        query = {
            'query': filters,
            'tweet.fields': 'created_at',
            'max_results': 100
        }

        if since_id is None:
            time_str = since_time.isoformat()
            query["start_time"] = time_str
        else:
            query["since_id"] = since_id
        return urljoin(self._url, '/2/tweets/search/recent') + '?' + urlencode(query)

    def _check_if_success(self, response):
        if not response.ok:
            raise Exception(f'HTTP {response.status_code} response')

    def get_all_tweets_since(self, time, since_id, users):
        r = self._get_oauth2_session().get(self._fetch_url(time, since_id, users))
        self._check_if_success(r)
        raw = r.json()
        if "data" in raw:
            # Ignoring responses
            result = [item for item in raw["data"] if "in_reply_to_status_id" not in item]
            result.reverse()
            return result
        else:
            return []

    def retweet(self, tweet_id):
        r = self._get_oauth1_session().post(self._retweet_url(tweet_id))
        self._check_if_success(r)
        return r.json()
