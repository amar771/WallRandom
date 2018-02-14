from praw import Reddit
from decouple import config
from wget import download
from random import choice
from time import time

# OS functions
from os import listdir
from os import rename

# Setup for using praw
r = Reddit(client_id=config("CLIENT_ID", default=''),
           client_secret=config("CLIENT_SECRET", default=''),
           password=config("PASSWORD", default=''),
           user_agent=config("USER_AGENT", default=''),
           username=config("USERNAME", default=''))

# Tries logging in as the user
try:
    r.user.me()

except:
    print("Authentification error.")

r.read_only = config("READ_ONLY", default=True, cast=bool)

sub = r.subreddit('wallpaper')
urls = []

# Stores links that are either
for submission in sub.hot(limit=25):
    valid_links = ['.png', '.jpg']
    if any(link in submission.url.lower() for link in valid_links):
        urls.append(submission.url)

final_link = choice(urls)
downloaded = False
while not downloaded:
    try:
        epoch_time = str(int(time()))
        filename = epoch_time + final_link[final_link.len() - 4:]
        print(filename)
        file = download(final_link, bar=None)
        downloaded = True
    except:
        final_link = choice(urls)
        print("Failed to download link {}".format(final_link))
