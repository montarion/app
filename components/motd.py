from time import sleep
import requests
import urllib
import praw
from random import *
import csv
class motd:
    def __init__(self, city):
        self.imagelink = ""
        self.songlink = ""
        self.headlines = []
        self.city = city
    def createmotd(self):
        self.reddit()
        self.song()
        sleep(1)
        fmotd = "Good morning! The weather in {0} " \
                "is [placeholder until you can get weather based on location], and it [doesn't seem like " \
                "the temperature will rise above/seems like the temperature will be higher than][average temp]," \
                "[but/so] let's make it a [stellar/good/great/...] day!" \
                "\nToday's news is that {1}[headline1 without url]. " \
                "\nAnd [last but not least/finally/now/...], here is today's song{2}[play on spotify?]"\
                .format(self.city, self.headlines[0][0], self.songlink)
        #possible right under news
        #"\n\n[possible: You'll find these and more stories here: {1}[headlines with url]]"

        return fmotd
    def reddit(self):
        client_id = "id"
        client_secret = "secret"
        username = "username"
        password = "password"
        user_agent = "testscript by /u/montarion"
        reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, password=password, username=username, user_agent=user_agent)
        
        #multireddit = reddit.multireddit(
        multi = reddit.multireddit('montarion', 'takemethere').top('day', limit=1)
        for thing in multi:
            
            self.imagelink = thing.url #idea: display image urls on greyhawk?
        
        sub = reddit.subreddit('tech').hot(limit=1)
        news = []
        for thing in sub:
            news.append(thing.title)
            news.append(thing.permalink)
            self.headlines.append(news)
        
        sub = reddit.subreddit('worldnews').hot(limit=1)
        news = []
        for thing in sub:
            news.append(thing.title)
            news.append(thing.permalink)
            self.headlines.append(news)

    def song(self):
        vidlist = []
        
        with open('scriptlets/realvidlinks.csv', 'r') as f:
            reader = csv.reader(f, delimiter=',')
            vidlink = list(reader)
        
        choice = randint(0, len(vidlink))
        sotd = vidlink[choice][0]
        self.songlink = sotd

