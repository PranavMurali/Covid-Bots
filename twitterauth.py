import tweepy
import logging
import config

logger = logging.getLogger()

def create_api():
    auth = tweepy.OAuthHandler(config.api_token,config.api_secret)
    auth.set_access_token(config.auth_token,config.auth_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, 
        wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api