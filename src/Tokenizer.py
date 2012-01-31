#!/usr/bin/python2.7

"""
	Tokenizes words based on the context
	(Requires lot of tweaking and testing)
	Uses NLTK
"""

import nltk, re

## The Tokenizer class 
#
# 

class Tokenizer:
	__PATTERNS__ = '''([A-Z]\\.)+|([A-Za-z]+n[']t)|\\$?\\d+(\\.\\d+)?%?|\\w+(-\\w+)*|\\.\\.\\.|[][.,;"\?!():-_`]'''
	def __init__(self, patterns = None):
		if patterns:
			p = ''
			for pattern in patterns:
				p += pattern + '|'
			self.__PATTERNS__ = p + self.__PATTERNS__
	
	def sent_tokenize(self, text):
		return nltk.sent_tokenize(text)
	
	def word_tokenize(self, text):
		return nltk.regexp_tokenize(text, self.__PATTERNS__, flags = re.IGNORECASE)
	
	def tokenize(self, text):
		return [self.word_tokenize(sent) for sent in self.sent_tokenize(text)]

	def nltk_tokenize(self, text):
		return [nltk.word_tokenize(sent) for sent in nltk.sent_tokenize(text)]
