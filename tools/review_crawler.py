#!/usr/bin/python
"""
Author: Ravindra Nath kakarla
Crawls reviews from various websites.
Supported websites
	Google product search
"""

import urllib2, sys, re
from BeautifulSoup import BeautifulSoup

urls = {
	"gps": "http://www.google.com/products/catalog?cid=$cid&os=reviews&start=$start&rtype=1"
}

reviews = []

if len(sys.argv) < 2:
	print "Usage: ", sys.argv[0], " <catalog id> [start_at = 0]"
	exit()

cid = sys.argv[1]
try:
	start = int(sys.argv[2])
except:
	start = 0

urls['gps'] = urls['gps'].replace('$cid', cid)
urls['gps'] = urls['gps'].replace('$start', str(start))

soup = BeautifulSoup(urllib2.urlopen(urls['gps']).read())

for i in range(0, 10):
	review_span = soup.find("span", {'id' : "uc-" + str(i)})
	if review_span is not None:
		review_text = review_span.text
		review_by = review_span.parent.findPreviousSibling("div", {"class": "review-rating"}).text
		regex = re.compile('By (.+) ', re.DOTALL)
		review_by = regex.search(review_by).group(1).split()[0]
		regex = re.compile('(\d)')
		review_rating = soup.find('div', {'class': 'review-rating'}).findChild().attrMap['title']
		review_rating = int(regex.search(review_rating).group(1))
		reviews.append({'user': review_by, 'rating': review_rating, 'raw-text': review_text})
