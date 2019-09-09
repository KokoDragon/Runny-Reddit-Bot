import praw
import re
import time
import requests
import sys


reddit = praw.Reddit(client_id = '5ShPOz-LuVRfXA',
                     client_secret = '_SlyyoPjxNITd5yEJ3neVWZW3b8',
                     user_agent = '<console:reddit_bot:0.0.1 (by /u/RunnyRedditBot)>',
                     username = 'RunnyRedditBot',
                     password = 'yoyoyo')


#reply a joke in response to a user commenting "!joke" using json
def run_bot(reddit,comments_replied_to):
    print("Obtaining your comments...")
    for comment in reddit.subreddit('test').comments(limit = 10):
        if "!joke" in comment.body and comment.id not in comments_replied_to: # and comment.author != reddit.user.me():
            print("String with \"!joke\" found!!")
            joke = requests.get('https://api.icndb.com/jokes/random').json()['value']['joke']
            comment.reply("You requested a joke! Here is the joke:\n\n" + joke)
            print("Comment ID: " + comment.id)
            comments_replied_to.append(comment.id)
            
            
    print("Pause for 10 seconds")
    time.sleep(10)

comments_replied_to = []
while True:
    if comments_replied_to:
        break
    run_bot(reddit, comments_replied_to)


#identify and post pictures on certain subreddits with time delay
subreddits = ['funny']
pos = 0
errors = 0

title = "Yeah this is pretty funny haha"
url = "https://imgur.com/gallery/T9vtMbj"

def post():
    global subreddits
    global pos
    global errors
    try:
        subreddit = reddit.subreddit(subreddits[pos])
        subreddit.submit(title, url = url)
        print("Posted to " + subreddits[pos])
        
        pos = pos + 1
        
        if (pos <= len(subreddits) - 1):
            post()
        else:
            print("Done")

    except praw.exceptions.APIException as e:
        if(e.error_type == "RATELIMIT"):
           delay = re.search("(\d+) minutes?", e.message)

           if delay:
               delay_seconds = float(int(delay.group(1))* 60)
               time.sleep(delay_seconds)
               post()
           else:
               delay = re.search("(\d+) seconds", e.message)
               delay_seconds  = float(delay.group(1))
               time.sleep(delay_seconds)
               post()

    except:
        errors = errors + 1
        if(errors > 5):
            print("Crashed")
            exit(1)

post()


#print comments in a stream (continuously) from subreddit
subreddit = reddit.subreddit('politics')
for comment in subreddit.stream.comments():
    try:
        print(comment.body)

        
    except praw.exceptions.PRAWException as e:
        pass 

#print comments from hot posts of a subreddit that are not stickied
hot_python = subreddit.hot(limit = 5)
for submission in hot_python:
    
    if not submission.stickied:
        comments = submission.comments
        for comment in comments:
            print(20* '-')
            print(comment.body)
            
            if len(comment.replies) > 0:
                for reply in comment.replies:
                    print('Reply: ', reply.body)
            


