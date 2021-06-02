import logging
import time
import sys

from config import config
from twitter_api import TwitterApi


running = True


def main():
    logging.basicConfig(
        stream=sys.stdout,
        level=config.app.log.level,
        format='[%(asctime)s] %(name)s: %(levelname)s - %(message)s'
    )
    log = logging.getLogger(config.app.name)
    log.info('Application started')

    retry_connect = config.app.retryConnectSeconds
    api = TwitterApi()

    while running:
        try:
            log.info('Opening stream')
            stream = api.stream(config.userIds)
            log.info('Stream opened')

            for tweet in stream:
                log.info(f'New tweet: {tweet.id}')
                api.retweet(tweet.id)
        except Exception as e:
            log.exception(e)

        log.info(f'Stream closed, waiting {retry_connect} seconds')
        time.sleep(retry_connect)


if __name__ == '__main__':
    main()
