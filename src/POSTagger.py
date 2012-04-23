#!/usr/bin/python2.7

"""
	Performs Parts of Speech tagging on the review text	
	Uses NLTK
"""
import nltk

class POSTagger:
	def nltk_tag(self, tokens):
		"""
			Uses the NLTK POS tagger to tag the tokens.
			tokens: List of tokens to be tagged.
		"""
		return nltk.pos_tag(tokens)
	
	def stemmer(self, tokens, type_ = 'plurals'):
		"""
			Uses NLTK WordNetLemmatizer to lemmatize and stem the tokens
			tokens: List of tokens to be lemmatize
			type_: type of operation (default: converts plurals to singulars)
		"""
		if type_ == 'plurals':
			#@see nltk.WordNetLemmatizer
			wnl = nltk.WordNetLemmatizer()
			return [wnl.lemmatize(token) for token in tokens]

	def train(self, testcases):
		#Todo 
		None
	
	def default_tag(self, wordtag_dict):
		#todo
		None

