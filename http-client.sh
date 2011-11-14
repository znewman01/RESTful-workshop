#!/bin/sh

# This is the hands-on part of the  talk

#######
# cURL
#######

# Basics: Let's see what our HTTP requests look like
curl "http://djce.org.uk/utils/echo.cgi"
# POST with data
curl -d "name=zack&password=12345" "http://djce.org.uk/utils/echo.cgi"
# POST with URL-encoded data
curl --data-urlencode "name=zack&password=12345 ?" "http://djce.org.uk/utils/echo.cgi"

# Twitter!
curl "http://api.twitter.com/1/statuses/user_timeline.xml?count=1&screen_name=50cent"

