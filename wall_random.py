from praw import Reddit
from decouple import config
from wget import download
from random import choice
from time import time

# OS functions
from os import listdir
from os import rename
from os import path
from os import makedirs

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

subs = config("SUBREDDITS",
              cast=lambda v: [s.strip() for s in v.split(',')])

sub = r.subreddit(choice(subs))


# Stores links that are either
def get_images_urls():
    urls = []
    for submission in sub.hot(limit=25):
        valid_links = ['.png', '.jpg']
        if any(link in submission.url.lower() for link in valid_links):
            urls.append(submission.url)

    return urls


def download_image(urls):

    if not path.exists("/tmp/wallrandom/"):
        makedirs("/tmp/wallrandom/")

    final_link = choice(urls)
    downloaded = False
    while not downloaded:
        try:
            # epoch_time = str(int(time()))
            # filename = epoch_time + final_link[final_link.len() - 4:]
            # print(epoch_time)
            download(final_link, out="/tmp/wallrandom/", bar=None)
            downloaded = True
        except:
            final_link = choice(urls)
            print("Failed to download link {}".format(final_link))


if __name__ == "__main__":
    download_image(get_images_urls())
