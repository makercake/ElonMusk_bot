import praw
import os
import csv
import re
from datetime import datetime
from replit import db
from keep_alive import keep_alive
import time
import random

answer_list = ["You're fired", "$8 please", "I've laid off most of the staff, and Twitter's still running. Looks like they weren't necessary.", "You look stupid. Fired.", "If you really love the company, you should be willing to work here for free.", "You're fired, now pay me $8"]

trigger_list = ["Elon Musk", "elon musk", "Elon musk", "Elon Tusk", "Twitter", "twitter"]



def bot_login():
    reddit = praw.Reddit(
    client_id = os.getenv('client_id'),
    client_secret = os.getenv('client_secret'),
    username = os.getenv('username'),
    password = os.getenv('password'),
    user_agent = "<ElonMusk_bot>"
    )
    return reddit



def run_bot(reddit, comments_replied_to):
  print("Searching last 1,000 comments")
  
  for comment in reddit.subreddit("ProgrammerHumor").comments(limit=1000):
    res = any(ele in comment.body for ele in trigger_list)
    
    if res == True and comment.id not in comments_replied_to and comment.author != reddit.user.me():
      print("String with \"Elon Musk\" found in comment " + comment.id)

      answer = random.choice(answer_list)
      comment.reply(answer)
      
      print("Replied to comment " + comment.id + "\n" + answer)
    
      comments_replied_to.append(comment.id)

      with open ("comments_replied_to.txt", "a") as f:
        f.write(comment.id + "\n")

      sleep()
      
    else:
      print("comment id is in list")
      run_bot(reddit, comments_replied_to)

  print("\nSearch Completed.")

  print(comments_replied_to)

def sleep():
  print("\nSleeping for 10 min...")
 	
  time.sleep(600)

def get_saved_comments():
  if not os.path.isfile("comments_replied_to.txt"):
    comments_replied_to = []
  else:
    with open("comments_replied_to.txt", "r") as f:
      comments_replied_to = f.read()
      comments_replied_to = comments_replied_to.split("\n")
      comments_replied_to = [_f for _f in comments_replied_to if _f]

  return comments_replied_to

reddit = bot_login()
comments_replied_to = get_saved_comments()
print(comments_replied_to)

while True:
  run_bot(reddit, comments_replied_to)

keep_alive()
