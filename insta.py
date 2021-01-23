# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# Before Run anything you should download Geckodriver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re
import pandas as pd
import InstagramBot
import datetime
import Constant


insta = InstagramBot.InstagramBot('username', 'password')
insta.login()

insta.UpdateMyFollowersFile()
insta.FetchSourcePagePosts()
insta.FetchSourcePagePostsLikers()
insta.UpdateLikersByFollowers()
insta.FolloweLikers()

