#!/usr/bin/python2.7

"""
	Find all useful opinion sentences containing frequent features
	Uses NLTK
"""
from nltk.corpus import WordListCorpusReader

class OpinionSentenceFinder:
	def __init__(self, features, feature_sentences):
		"""
			Filter all the sentences containing frequent features
			features: List of frequent features
			feature_sentences: List of all sentences containing features

		"""
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
		"""
			Initializes the Opinion-Miner corpora.
		"""
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
	"""
	def get_nearest_JJ(self, tags, n_index):
		"""
			Finds the most probable adjective describing the the given feature in a sentence.
			tags: List of POS tags of given sentence.
			n_index: List index of the feature word.
			
			Algorithm:
				Start from the feature token (n_index) and move to the right till one of the following is found:
					i) A sentence end marker (and, ',', '.', or etc.)
					ii) An adjective tag ('JJ', 'JJS', 'JJR')
					if a negation word in found:
						set neg flag to w, where w is the negation word
					If the obtained adjective is in positive words corpus:
						set sentiment_right = positive
					else If the obtained adjective is in negative words corpus:
						set sentiment_right = negative
					else	
						set sentiment_right = None
					index_right = index of adjective_token
				
				Repeat the above process proceeding to the left of feature token
					index_left = index of adjective_token
					Find the sentiment_left using the above process
				
				if n_index - index_left < n_index - index_right:
					sentiment = sentiment_left
				else:
					sentiment = sentiment_right
				
				if neg is set:
					sentiment = !sentiment
				
				return adjective, sentiment
				
			
		"""
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
