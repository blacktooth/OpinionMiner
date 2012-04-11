#!/usr/bin/python2.7

"""
	Find all useful opinion sentences containing frequent features
	Uses NLTK
"""

from nltk.corpus import WordListCorpusReader

class OpinionSentenceFinder:
	def __init__(self, features, feature_sentences):
		self.feature_sentences = feature_sentences
		self.opinion_sentences = []
		self.features = features
		self.__init_corpora()
		for sent_index in xrange(len(self.feature_sentences)):
			sent = self.feature_sentences[sent_index]
			self.feature_sentences[sent_index]['opinion_sent'] = []
			for feature in self.features:
				feature = feature[0]
				if feature in sent['nouns'] or feature in sent['noun_phrases']:
					for index in xrange(len(sent['tags'])):
						(w, t) = sent['tags'][index]
						if w.find(feature.split()[0]) > -1:
							JJ = self.get_nearest_JJ(sent['tags'], index)
							self.feature_sentences[sent_index]['opinion_sent'].append((feature, JJ))
							self.opinion_sentences.append((feature, JJ))
		
	def __init_corpora(self):
		self.negation_words = WordListCorpusReader('../data/corpora/', 'negation_words')
		self.sent_ends = WordListCorpusReader('../data/corpora', 'sent_ends')
		self.negative_sentiments = WordListCorpusReader('../data/corpora/sentiment-lexicon', 'negative-words.txt')
		self.positive_sentiments = WordListCorpusReader('../data/corpora/sentiment-lexicon', 'positive-words.txt')

					
	def remove_uncertain_features(self):
		None
	"""
		Todo: concat consecutive JJ's (Opt.) 
		      Remove meaningless JJ's (95% done.)
		      Implement lemmatizing while checking JJ's
		      Stop scanning for JJ's, after the period or ',' or other sentence ends (done.)
		      Negation of opinions. (done.)
		      (Opt.) Append (RR, RB) to the JJ
		      Special treatment for NOUNS in pros
			Fix neg bug
	"""
	def get_nearest_JJ(self, tags, n_index):
		adj = ''
		neg = ''
		sentiment = None
		for i in xrange(n_index + 1, len(tags)):
			(w, t) = tags[i]
			if w in self.sent_ends.words():
				break
			if w in self.negation_words.words():
				neg = w
			if t in ['JJ', 'JJR', 'JJS']:
				adj = w
			if unicode.encode(w) in self.negative_sentiments.words():
				adj = w
				sentiment = False
			if unicode.encode(w) in self.positive_sentiments.words():
				adj = w
				sentiment = True
				break
		start = n_index
		if len(adj) < 1:
			end = -1
			neg = ''
		else:
			end = n_index - (i - n_index) - 1
		for j in xrange(start, end, -1):
			(w, t) = tags[j] 
			if w in self.sent_ends.words():
				break
			if w in self.negation_words.words():
				neg = w
			if t in ['JJ', 'JJR', 'JJS']:
				adj = w
			if unicode.encode(w) in self.negative_sentiments.words():
				adj = w
				sentiment = False
			if unicode.encode(w) in self.positive_sentiments.words():
				adj = w
				sentiment = True
				break
		if len(neg) > 1:
			sentiment = not sentiment
		return (sentiment, neg, adj) 
