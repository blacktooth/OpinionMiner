#!/usr/bin/python2.7

"""
	Performs Parts of Speech tagging on the review text	
	Uses NLTK
"""

import nltk

## The POSTagger class 
#
# 
class POSTagger:
	def nltk_tag(self, tokens):
		return nltk.pos_tag(tokens)
	
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

