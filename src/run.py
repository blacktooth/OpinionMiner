#!/usr/bin/python
from ReviewParser import ReviewParser
from FeatureExtractor import FeatureExtractor
from subprocess import check_output
import sys

try: 
	min_support = int(sys.argv[1])
except:
	min_support = 5

reviews_path = '../data/reviews/'
review_files = check_output(['ls', '-1', reviews_path]).split()

for review_file in review_files:
	print review_files.index(review_file), ' ' + review_file

choice = int(input('#'))
if choice not in xrange(0, len(review_files)):
	print 'Error'
	exit(-1)

rev = ReviewParser(open(reviews_path + review_files[choice], 'rb',), review_files[choice].split('.')[-1])

rev.parse()

text = rev.get_raw_text()

f = FeatureExtractor(text, review_files[choice])

print "Based on ", len(rev.reviews), " reviews"

features = f.get_frequent_features(min_support)

features = f.prune_features(features, 3)
print "Is this a %s?" % f.product_category
