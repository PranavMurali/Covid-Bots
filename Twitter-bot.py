import tweepy
import logging
from twitterauth import create_api
import time
from covid import Covid
covid = Covid()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def check_mentions(api, keywords, since_id):
    logger.info("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline,
        since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            continue
        if "data" in tweet.text.lower():
            logger.info(f"Answering to {tweet.user.name}")
            
            if not tweet.user.following:
                tweet.user.follow()
            txt=tweet.text.lower()
            c=txt.split()[2]
            coun= covid.get_status_by_country_name(c)
            active = coun.get('active')       
            act='\U0001F915'             
            conf = coun.get('confirmed')
            con='\U0001F637'
            death = coun.get('deaths')
            ded='\U00002620'
            recv = coun.get('recovered')
            rec='\U0001F3E5'
            api.update_status(
                status="The COVID-19 data for "+c+":"+"\n"+act+"Active cases: {:,}".format(active) + "\n" +con+ "Confirmed cases: {:,}".format(conf) + "\n" +rec+ "Recovered cases: {:,}".format(recv)+ "\n" +ded+ "No.of Deaths: {:,}".format(death),
                in_reply_to_status_id=tweet.id,
                auto_populate_reply_metadata=True
            )

    return new_since_id

def main():
    api = create_api()
    since_id = 1
    while True:
        since_id = check_mentions(api, ["data"], since_id)
        logger.info("Waiting...")
        time.sleep(10)

if __name__ == "__main__":
    main()