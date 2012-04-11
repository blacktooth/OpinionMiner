#!/usr/bin/python
from ReviewParser import ReviewParser
from FeatureExtractor import FeatureExtractor
from subprocess import check_output
from OpinionSentenceFinder import OpinionSentenceFinder
import sys, pprint
import settings


class OpinionMiner:
	def __init__(self, cid, min_support = 5):
		self.cid = cid
		self.min_support = min_support
		self.ratings = {}
		self.features = []

	def run(self):
		rev = ReviewParser(open(settings.reviews_path + ReviewParser.map_cid_to_name(self.cid), 'rb',), review_files[choice].split('.')[-1])
		rev.parse()

		print "Mining", len(rev.reviews), "reviews"

		text = rev.get_raw_text()

		f = FeatureExtractor(text, ReviewParser.map_cid_to_name(self.cid))

		self.features = f.get_frequent_features(self.min_support)
		
		for ftr in self.features:
			self.ratings[ftr[0]] = {'positive': 0, 'negative': 0, 'neutral': 0}

		o = OpinionSentenceFinder(self.features, f.feature_sentences)

		#Extract all sentences which express some opinion
		opinion_sents = map(lambda y: y['opinion_sent'], filter(lambda x: len(x['opinion_sent']) > 1, o.feature_sentences))
		
		temp = []
	
		for os in opinion_sents:
			temp.extend(os)		

		opinion_sents = temp
		
		for ftr, sentiment in opinion_sents:
			if sentiment[0] is True:
				self.ratings[ftr]['positive'] += 1
			elif sentiment[0] is False:
				self.ratings[ftr]['negative'] += 1
			else:
				self.ratings[ftr]['neutral'] += 1

		pp = pprint.PrettyPrinter(indent = 4)
		print "Is this a %s?" % f.product_category
		print "%d features are interesting" % len(self.features)

		#pp.pprint(opinion_sents)
		pp.pprint(self.ratings)


if __name__ == "__main__":
	try: 
		min_support = int(sys.argv[1])
	except:
		min_support = 4
	review_files = ReviewParser.get_available_reviews()
	for review_file in review_files:
		print review_files.index(review_file), ' ' + review_file
	choice = int(input('#'))
	if choice not in xrange(0, len(review_files)):
		print 'Error'
		exit(-1)

	cid = review_files[choice].split(".")[0].split("_")[-2] 
	om = OpinionMiner(cid, min_support)
	om.run()

