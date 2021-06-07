import logging
import time
import signal
import sys
from datetime import datetime, timezone, timedelta
from dateutil import parser

import config
from twitter_api import TwitterApi


running = True


def main():
    cfg = config.get_config()

    logging.basicConfig(
        stream=sys.stdout,
        level=cfg["app"]["log"]["level"],
        format='[%(asctime)s] %(name)s: %(levelname)s - %(message)s'
    )
    log = logging.getLogger(cfg["app"]["name"])

    api = TwitterApi()

    log.info('Application started')
    main_loop(log, cfg, api)


def main_loop(log, cfg, api):
    retry_connect = cfg["app"]["retry_connect_seconds"]
    fetch_interval = cfg["app"]["fetch_interval_seconds"]
    users = cfg["users"]

    last_timestamp = datetime.now(tz=timezone.utc) - timedelta(seconds=fetch_interval)
    since_id = None
    while running:
        try:
            log.debug('Fetching tweets')
            tweets = api.get_all_tweets_since(last_timestamp, since_id, users)
            log.debug(f'Fetched {len(tweets)} tweets')

            for tweet in tweets:
                api.retweet(tweet["id"])

            if tweets:
                since_id = tweets[0]["id"]
                last_timestamp = None

            log.debug(f'Waiting {fetch_interval} seconds')
            time.sleep(fetch_interval)
        except Exception as e:
            log.exception(e)
            log.info(f"Waiting {retry_connect} due to error")
            time.sleep(retry_connect)


if __name__ == '__main__':
    main()
