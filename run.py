from tweepy import StreamListener
from tweepy import Stream
import tweepy
import json
from screenshot import screenshot
from dbxup import save_to_dropbox

# Twitter Keys
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())


class StdOutListener(StreamListener):

    def on_data(self, data):
        x = json.loads(data)
        try:
            post_time = x['created_at']
            print('[*] New post detected at: %s' % post_time)
            print('    Post Text: %s' % x['text'])
            url = 'https://www.twitter.com/' + screen_name + '/status/' + x['id_str']
            filepath = 'screenshots/' + screen_name + '_' + x['id_str'] + '.png'
            screenshot(url, filepath, resolution=[1920, 1080])
            save_to_dropbox(filepath)
        except KeyError:
            pass

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    screen_name = '' # Twitter Username
    user = api.get_user(screen_name=screen_name)
    user_id = str(user['id'])

    listener = StdOutListener()
    twitterStream = Stream(auth, listener)
    twitterStream.filter(follow=[user_id])
