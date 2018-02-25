# WallRandom

Gets random wallpaper from specified subreddits and sets it as background every time you log in to your account.

### Installation

    $ sudo apt install feh

    $ git clone wallrandom
    $ cd wallrandom
    $ sudo chmod u+x wallrandom.sh
    $ python3 -m venv venv/
    $ source venv/bin/activate
    (venv)$ pip3 install -r requirements.txt
    (venv)$ python wallrandom.py --settings

Edit the wallrandom.sh file with the directory to the wallrandom.py

Add wallrandom.sh to one of these starting from top:

    ~/.bash_profile
    ~/.bash_login
    ~/.profile

###### TODO:

- [x] PRAW works, user authenticates properly 
- [x] Gets random wallpaper from a subreddit
- [x] Works with multiple subreddits
- [x] Can set the directory to save files to
- [x] Sets the downloaded file to background
- [x] Can specify to either save or delete the wallpapers after use
- [] Add CLI parameters/functions
- [] Add custom logging
