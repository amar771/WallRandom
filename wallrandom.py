from praw import Reddit
from decouple import config
from wget import download
from random import choice
from time import time

# OS functions
from os import listdir
from os import path
from os import makedirs
from os import unlink
from os import system

from shutil import copyfile


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
directory = config("DIRECTORY", default="/tmp/wallrandom/")

save = config("SAVE", default=True, cast=bool)
save_path = config("SAVE_PATH", default="~/Pictures/WallRandom/")


# Stores links that are either
def get_images_urls():
    '''Gets url from image'''
    urls = []
    for submission in sub.hot(limit=25):
        valid_links = ['.png', '.jpg']
        if any(link in submission.url.lower() for link in valid_links):
            urls.append(submission.url)

    return urls


def remove_from_tmp():
    '''Cleans tmp directory from other images so the script can
    set it as background.
    '''
    if not path.exists(directory):
        return True

    else:
        for image in listdir(directory):
            image_path = path.join(directory, image)
            if any(file in str(image) for file in ['.png', '.jpg']):
                try:
                    if path.isfile(image_path):
                        unlink(image_path)

                except:
                    print("Unable to delete {}".format(image_path))


def copy_image():
    '''Copies image from temporary directory to permanent one'''
    if not path.exists(save_path):
        makedirs(save_path)

    for image in listdir(directory):
        image_path_tmp = path.join(directory, image)
        image_path_perm = path.join(save_path, image)
        if any(file in str(image) for file in ['.png', '.jpg']):
            try:
                copyfile(image_path_tmp, image_path_perm)

            except:
                print("Unable to copy file to permanent location")


def set_as_background():
    '''
    Sets downloaded image as a background image
    Uses feh to do the job
    '''
    if len(listdir(directory)) == 1:
        image = listdir(directory)[0]
        image_path = path.join(directory, image)

        if '.jpg' in image or '.png' in image:
            command = 'feh --bg-fill {}'.format(image_path)
            system(command)


def download_image(urls):
    '''Downloads image with current epoch as name'''
    if not path.exists(directory):
        makedirs(directory)

    final_link = choice(urls)
    downloaded = False
    while not downloaded:
        try:
            epoch_time = str(int(time()))
            filename = epoch_time + final_link[len(final_link) - 4:]

            file = directory + filename

            download(final_link, out=file, bar=None)
            downloaded = True
        except:
            final_link = choice(urls)
            print("Failed to download link {}".format(final_link))


def user_input(separated):
    bool_questions = ["True", "False"]
    print("Enter {} (\"{}\")".format(separated[0], separated[1]),
          end='',
          flush=True)

    if separated[1] in bool_questions:
        bad_input = True
        print()
        while bad_input:
            print("Please enter Yes/No ",
                  end='',
                  flush=True)

            user = str(input("[Blank for default] # --> "))
            if not user:
                bad_input = False

            elif user.lower()[0] is "y":
                user = "True"
                bad_input = False

            elif user.lower()[0] is "n":
                user = "False"
                bad_input = False

            else:
                bad_input = True

    else:
        user = str(input("[Blank for default] # --> "))

    # if input is blank
    if not user:
        return separated[1]

    return user


def settings():
    '''Settings for the application'''
    # Read all non comment lines from .env.example file
    example_env = []
    with open(".env.example", "r") as file:
        for line in file:
            if line[0] is not "#":
                fixed_line = line[:len(line) - 1]
                example_env.append(fixed_line)

    # Write to .env file
    with open(".env", "w") as file:
        for line in example_env:
            # If line is empty just copy it
            if not line:
                file.write(line)
                file.write("\n")
            # Else separate it in variable and value and ask for input
            else:
                separated = line.split("=")
                file.write(separated[0])
                file.write("=")

                user = user_input(separated)
                file.write(user)
                file.write("\n")


if __name__ == "__main__":
    something = True
    if something:
        remove_from_tmp()
        download_image(get_images_urls())
        set_as_background()

        if save:
            copy_image()

    else:
        settings()
