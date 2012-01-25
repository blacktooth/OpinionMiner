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
	def __init__(self, tokens):
		if type(tokens) is not type([]):
			t = WordTokenizer()
			self.tokens = t.tokenize(tokens)
		else:
			self.tokens = tokens
			
	def nltk_tag(self):
		return nltk.pos_tag(self.tokens)
	
	def train(self, testcases):
		#Todo 
	
	def default_tag(self, wordtag_dict):
		#todo

