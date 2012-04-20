#!/usr/bin/python2.7

"""
	Extracts features from the reviews
	Uses NLTK
"""

from Tokenizer import Tokenizer
from POSTagger import POSTagger
from ReviewParser import ReviewParser
from nltk import FreqDist
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords, wordnet

class FeatureExtractor:
	def _remove_stopwords(self, tokens):
		words = stopwords.words('english')
		#Find a way to eliminate the need for adding custom stopwords
		words.extend(['pros', 'cons', 'things', 'day', 'points', 'time', 'month', 'year'])
		return [token.lower() for token in tokens if token.lower() not in words and len(token) > 1]

	def __init__(self, text, product_name):
		self.candidate_features = []
		self.feature_sentences = []
		self.product_name = ReviewParser.get_pretty_name(product_name)
		t = Tokenizer()
		sents = t.sent_tokenize(text.lower())
		p = POSTagger()
		wnl = WordNetLemmatizer()
		for sent in sents:
			tagged_sent = p.nltk_tag(t.word_tokenize(sent))
			feature_sent = {}
			feature_sent['sentence'] = sent
			feature_sent['tags'] = tagged_sent
			feature_sent['nouns'] = []
			feature_sent['noun_phrases'] = []
			for i in range(0, len(tagged_sent)):
				(word, tag) = tagged_sent[i]
				#Don't include proper nouns
				if tag.startswith('N') and tag != 'NNP':
					"""
					Consecutive nouns might form a feature phrase. Eg. Picture quality is a phrase.
					Meaningless phrases like 'quality digital' are removed later as their frequeny of occurence is	low. """
					if i > 0 and len(feature_sent['nouns']) > 0 and tagged_sent[i - 1][0] == feature_sent['nouns'][-1] and feature_sent['sentence'].find(feature_sent['nouns'][-1] + ' ' + word) > -1:
						feature_sent['noun_phrases'].append(wnl.lemmatize(feature_sent['nouns'].pop() + ' ' + word))
					else:
						feature_sent['nouns'].append(wnl.lemmatize(word))
					
			self.feature_sentences.append(feature_sent)

	def candidate_feature_list(self):
		for fs in self.feature_sentences:
			self.candidate_features.extend(list(set(fs['nouns'])))
			self.candidate_features.extend(list(set(fs['noun_phrases'])))
		return self.candidate_features

	def prune_features(self, features, p_support):
		
		#The most frequent feature is the type of product (from many observations)
		self.product_category = features.pop(0)[0]

		#Find a way to eliminate the need for adding custom words 
		words = ['pro', 'con', 'thing', 'day', 'point', 'time', 'month', 'year']
		#Eliminate words that represent the name of the product
		words.extend(self.product_name.split())

		features = filter(lambda x: len(x[0]) > 2 and x[0] not in words, features)

		#Map 1 word features to their supersets (Eg. battery to battery life)
		#Currently works for 1 word to 2 word phrase mapping.
		#Disagreed with p_support issue from paper
		for i in xrange(0, len(features)):
			for j in xrange(0, len(features)):
				if features[i][0] in features[j][0].split():
					features[i] = features[j]


		return sorted(list(set(features)), key=lambda x: x[1], reverse=True)
		
	"""
		This method differs from paper
	"""
	def get_frequent_features(self, min_support):
		#get n item sets	
		dist = FreqDist(self.candidate_feature_list())
		features = [(item, count) for (item, count) in dist.iteritems() if count >= min_support]
		return self.prune_features(features, 3)
