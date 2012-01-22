#!/usr/bin/python2.7

"""
Parse reviews from all supported formats (JSON, CSV, XML...)
	
"""

import sys, csv, json


"""
Check for proper python version and running environment
"""


## The review parser class
#
# Parse reviews from all supported formats (JSON, CSV, XML) to tuples
class ReviewParser:

	def __init__(self, handle, format_, delimiter = ','):
		self.reviews = []
		self.format_ = format_
		self.handle = handle 
		self.CSV_DELIM = delimiter

	## Parse method
	#
	# 
	def parse(self):
		if self.handle is None or self.format_ is None:
			raise AttributeError
		
		if self.format_ == 'CSV':
			reviews = csv.reader(self.handle, delimiter = self.CSV_DELIM, quotechar = '|')
			for review in reviews:
				self.reviews.append((review[0], review[1], review[2]))

		elif self.format_ == 'JSON':
			reviews = json.load(self.handle)
			for review in reviews:
				self.reviews.append((review['comment-by'], review['comment-rating'], review['comment-text']))

		elif self.format_ == 'XML':
			#parse XML
		else:
			raise AttributeError

		return self.reviews
