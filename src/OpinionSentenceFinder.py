#!/usr/bin/python2.7

"""
	Find all useful opinion sentences containing frequent features
	Uses NLTK
"""

class OpinionSentenceFinder:
	def __init__(self, features, feature_sentences):
		self.feature_sentences = feature_sentences
		self.features = features
		for sent_index in xrange(len(self.feature_sentences)):
			sent = self.feature_sentences[sent_index]
			self.feature_sentences[sent_index]['opinion_sent'] = []
			for feature in self.features:
				feature = feature[0]
				if feature in sent['nouns']:
					for index in xrange(len(sent['tags'])):
						(w, t) = sent['tags'][index]
						if w.find(feature) > -1:
							self.feature_sentences[sent_index]['opinion_sent'].append((w, self.get_nearest_JJ(sent['tags'], index)))
		
			
	"""
		Todo: concat consecutive JJ's 
		      Remove meaningless JJ's
		      Implement lemmatizing while checking JJ's
		      Stop scanning for JJ's, after the period or ','
		      Negation of opinions
	"""
	def get_nearest_JJ(self, tags, n_index):
		adj = None
		sent_ends = ['.', ',', '!', ':', ';', '|']
		for i in xrange(n_index + 1, len(tags)):
			(w, t) = tags[i]
			if t in ['JJ', 'JJR', 'JJS']:
				adj = w
				break

		for j in xrange(n_index, -1, -1):
			(w, t) = tags[j] 
			if not i - n_index >= n_index - j:
				break
			else:
				if t in ['JJ', 'JJR', 'JJS']: 
					adj = w
					break
		return adj

				
		
