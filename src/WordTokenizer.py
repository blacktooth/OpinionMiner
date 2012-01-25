#!/usr/bin/python2.7

"""
	Tokenizes words based on the context
	(Requires lot of tweaking and testing)
	Uses NLTK
"""

import nltk

## The WordTokenizer class 
#
# 

class WordTokenizer:
	self.__PATTERNS__ = '''([A-Z]\\.)+|\\w+(-\\w+)*|\\$?\\d+(\\.\\d+)?%?|\\.\\.\\.|[][.,;"\'?!():-_`]'''
	def __init__(self, patterns = None):
		if patterns:
			p = ''
			for pattern in patterns:
				p += pattern + '|'
			self.__PATTERNS__ = p + self.__PATTERNS__
	
	def sent_tokenize(self, text):
		return nltk.sent_tokenize(text)
	
	def word_tokenize(self, text):
		return nltk.regexp_tokenize(text, self.__PATTERNS__)
	
	def tokenize(self, text):
		return [self.word_tokenize(sent) for sent in self.sent_tokenize(text)]

	def nltk_tokenize(self, text):
		return [nltk.word_tokenize(sent) for sent in nltk.sent_tokenize(text)]
		
