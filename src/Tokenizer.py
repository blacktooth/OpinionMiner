#!/usr/bin/python2.7

"""
	Tokenizes words based on the context
	(Requires lot of tweaking and testing)
	Uses NLTK
"""

import nltk, re
from nltk import WhitespaceTokenizer


class Tokenizer:
	__PATTERNS__ = '''([A-Za-z]+n[']t)|\\$?\\d+(\\.\\d+)?%?|\\w+(-\\w+)*|\\.\\.\\.|[][.,;"\?!():-_`]'''
	def __init__(self, patterns = None):
		"""
			Initializes the tokenizer
			patterns: Regular expressions patterns to use
		"""
		if patterns:
			p = ''
			for pattern in patterns:
				p += pattern + '|'
			self.__PATTERNS__ = p + self.__PATTERNS__
	
	def sent_tokenize(self, text):
		"""
			Uses NLTKs sent_tokenize to tokenize paragraphs to sentences
			text: List of paragraphs
		"""
		return nltk.sent_tokenize(text)
	
	def word_tokenize(self, text):
		"""
			Tokenizes the words using the NLTKs regular expression tokenizer
			text: List of paragraphs
		"""
		return nltk.regexp_tokenize(text, self.__PATTERNS__, flags = re.IGNORECASE)

	def whitespace_tokenize(self, text):
		"""
			Tokenizes the words using the NLTKs whitespace tokenizer
			text: List of paragraphs
		"""
		wst = WhitespaceTokenizer()
		return wst.tokenize(text)
	
	def tokenize(self, text):
		"""
			Default tokenizer method
			text: List of paragraphs
		"""
		return [self.word_tokenize(sent) for sent in self.sent_tokenize(text)]

	def nltk_tokenize(self, text):
		return nltk.word_tokenize(text)
