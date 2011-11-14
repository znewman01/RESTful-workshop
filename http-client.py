#!/usr/bin/python

# This is the hands-on part of the  talk

# You need to get this library first:
#     pip install requests
# That easy! As long as you have pip
# virtualenv recommended
import requests

# Just see basic requests
echo = "http://djce.org.uk/utils/echo.cgi"
r = requests.get(echo)
print r.content

# See a POST request
payload = {'username': 'zack', 'password': 'squeamishossifrage'}
r = requests.post(echo, data=payload)
print r.content

# Twitter! See what Fiddy is up to
twitter = "http://api.twitter.com/1/statuses/user_timeline.xml"
twitter_params = "?count=1&screen_name=50cent"
r = requests.get(twitter + twitter_params)
print r.content
