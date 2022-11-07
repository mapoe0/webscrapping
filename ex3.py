import tweepy
from dotenv import load_dotenv
import os
import time

# environment variable

load_dotenv()
api_key = os.getenv("api_key")
api_key_secret = os.getenv("api_key_secret")
acces_token = os.getenv("acces_token")
acces_token_secret = os.getenv("acces_token_secret")
bearer_token = os.getenv("bearer_token")
# connect to the client
client = tweepy.Client(
    bearer_token=bearer_token,
    consumer_key=api_key,
    consumer_secret=api_key_secret,
    access_token=acces_token,
    access_token_secret=acces_token_secret
)
# auth to account using OAuth1
auth = tweepy.OAuth1UserHandler(api_key, api_key_secret, acces_token, acces_token_secret)
api = tweepy.API(auth)
# if throw exeption = auth failed
api.verify_credentials()
###
# QUESTION 1
# Scrape Emmanuel Macron first tweet.
#
###
userId = "EmmanuelMacron"
tweets = api.user_timeline(screen_name=userId,
                           # 200 is the maximum allowed count
                           count=1,
                           include_rts=False,
                           # Necessary to keep full_text
                           # otherwise only the first 140 words are extracted
                           tweet_mode='extended'
                           )
f = open("result/exo3/last_tweet_macron.txt", "w", encoding='utf-8')
# print and save
for info in tweets[:3]:
    print("ID: {}".format(info.id))
    print(info.created_at)
    print(info.full_text)
    print("\n")
    f.write(f"ID: {info.id}\n")
    f.write(f"{info.created_at}\n")
    f.write(info.full_text)
f.close()

# reset the file
open("result/exo3/tweets.txt", "w", encoding='utf-8').close()


class Listener(tweepy.StreamingClient):
    # to count the tweet
    cpt = 0
    # to store the tweet scrap
    f = open("result/exo3/tweets.txt", "a", encoding='utf-8')

    def on_tweet(self, tweet):
        self.cpt += 1
        print("tweet récup: " + str(self.cpt))
        # console print
        print(tweet.text)
        # save in file
        self.save(tweet.text)
        # adding delay to avoid spam
        time.sleep(1)

    def save(self, text):
        self.f.write(f"tweet scrap: n°{self.cpt}\n{text}\n\n")
        self.f.flush()

    def on_connect(self):
        print('connection started')

    def on_disconnect(self):
        print('connection stop')
        self.f.close()


keywords = ["#python", "coding"]
streaming_client = Listener(bearer_token=bearer_token)
# ## ISSUE there is an issue if we restart the program because of persisting rules
# the prog will keep the last rule in memory witch can create problems
# https://twittercommunity.com/t/how-does-filter-work-with-streaming-client/172174 according to this solution we need
# to delete it before adding new rules to the stream listener we need to add a try catch because if its the first
# time we execute the program, it will throw an exeption because of no rules will be foud
#
try:
    rules_ids = []
    for rule in streaming_client.get_rules().data:
        rules_ids.append(rule.id)
    if len(rules_ids) > 0:
        streaming_client.delete_rules(rules_ids)
except TypeError:
    pass
# then we can add our rules
for keyword in keywords:
    streaming_client.add_rules(tweepy.StreamRule(keyword))
streaming_client.filter()