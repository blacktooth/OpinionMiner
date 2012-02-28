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

f = FeatureExtractor(text)

print "Based on ", len(rev.reviews), " reviews"

print f.get_frequent_features(min_support)

"""
#tokenize_patterns = ['[Nn]ikon ?[dD][0-9]+', '([0-9]+ ?mm)', '(auto[ -_]?focus)', '(Apple)[ ]?(iphone)??[0-5]?[gs]*']
features = [w.lower() for (w,t) in tags if t.startswith('N') and t != 'NNP']

features = p.stemmer(features)

dist = nltk.FreqDist(features)

obs = [ob for ob in dist.iteritems()]

logfile = open('/tmp/log.txt', 'w')
logfile.write("".join(str(obs)).replace("), (", ")\n("))
logfile.close()
"""
