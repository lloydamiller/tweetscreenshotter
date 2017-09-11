from tweepy import StreamListener
from tweepy import Stream
import tweepy
import json
import os
from selenium import webdriver

# Twitter API Keys
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())


def screenshot(url, filepath, resolution=[1024, 768]):
    # takes url, opens page using PhantomJS at specificed resolution,
    # takes screenshot and saves to filepath

    driver = webdriver.PhantomJS()
    width, height = resolution[0], resolution[1]
    driver.set_window_size(width, height)

    print('[*] Loading webpage @ %s' % url)
    driver.get(url)

    print('[*] Saving screenshot to %s' % filepath)
    driver.save_screenshot(filepath)

    print('[*] Screenshot saved locally')
    return


class StdOutListener(StreamListener):
    # Tweepy open streaming class

    def on_data(self, data):
        x = json.loads(data)
        try:
            post_time = x['created_at'] # only takes screenshots of NEW tweets
            print('[*] New post detected at: %s' % post_time)
            print('    Post Text: %s' % x['text'])
            url = 'https://www.twitter.com/' + screen_name + '/status/' + x['id_str']
            if not os.path.exists('screenshots'):
                os.makedirs('screenshots') # create screenshots folder if it doesn't exist
            file_path = 'screenshots/' + screen_name + '_' + x['id_str'] + '.png'
            screenshot(url, file_path, resolution=[1920, 1080]) # keep 16x9 aspect
        except KeyError:
            pass

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    screen_name = '' # Twitter Username
    user = api.get_user(screen_name=screen_name)
    user_id = str(user['id']) # Tweepy follows user ID, not username

    listener = StdOutListener()
    twitterStream = Stream(auth, listener)
    twitterStream.filter(follow=[user_id])
