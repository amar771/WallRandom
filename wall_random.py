from praw import Reddit
from decouple import config

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
