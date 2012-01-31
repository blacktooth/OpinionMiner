#!/usr/bin/python2.7

"""
	Performs Parts of Speech tagging on the review text	
	Uses NLTK
"""

import nltk, re

## The POSTagger class 
#
# 
class POSTagger:
	def __init__(self, tokens_list):
		self.tokens = []
		for tokens in tokens_list:
			for token in tokens:
				self.tokens.append(token)
			
	def nltk_tag(self):
		return nltk.pos_tag(self.tokens)
	
	def stemmer(self, tokens, type_ = 'plurals'):
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

