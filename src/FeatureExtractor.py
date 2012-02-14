#!/usr/bin/python2.7

"""
	Extracts features from the reviews
	Uses NLTK
"""

from Tokenizer import Tokenizer
from POSTagger import POSTagger
from nltk import FreqDist
from nltk import WordNetLemmatizer

class FeatureExtractor:
	def __init__(self, text):
		self.candidate_features = []
		self.feature_sentences = []
		t = Tokenizer()
		sents = t.sent_tokenize(text)
		p = POSTagger()
		for sent in sents:
			tagged_sent = p.nltk_tag(t.nltk_tokenize(sent))
			feature_sent = {}
			feature_sent['sentence'] = sent
			feature_sent['nouns'] = []
			feature_sent['noun_phrases'] = []
			for i in range(0, len(tagged_sent)):
				(word, tag) = tagged_sent[i]
				if tag.startswith('N') and tag != 'NNP':
					if i > 0 and len(feature_sent['nouns']) > 0 and tagged_sent[i - 1][0] == feature_sent['nouns'][-1]:
						feature_sent['noun_phrases'].append(feature_sent['nouns'].pop() + ' ' + word)
					else:
						feature_sent['nouns'].append(word)
					
			self.feature_sentences.append(feature_sent)

	def candidate_feature_list(self):
		for fs in self.feature_sentences:
			self.candidate_features.extend(fs['nouns'])
			self.candidate_features.extend(fs['noun_phrases'])
		return self.candidate_features

	
	"""
		This method differs from paper
	"""
	def get_frequent_features(self, min_support):
		#get n item sets	
		wnl = WordNetLemmatizer()
		features = [wnl.lemmatize(token) for token in self.candidate_feature_list()]
		dist = FreqDist(features)
		return [(item, count) for (item, count) in dist.iteritems() if count >= min_support]
