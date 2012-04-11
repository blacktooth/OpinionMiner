#!/usr/bin/python2.7

"""
	Parse reviews from all supported formats (JSON, CSV, XML...)
	
"""

import sys, csv, json
from subprocess import check_output
import settings

## The review parser class
#
# Parse reviews from all supported formats (JSON, CSV, XML) to a list of dicts
class ReviewParser:

	@staticmethod
	def get_available_reviews():
		review_files = check_output(['ls', '-1', settings.reviews_path]).split()
		return review_files

	@staticmethod
	def map_cid_to_name(cid):
		review_files = check_output(['ls', '-1', settings.reviews_path]).split()
		for rf in review_files:
			if rf.split('.')[0].split('_')[-2] == cid:
				return rf

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
		
		if self.format_ == 'csv':
			reviews = csv.reader(self.handle, delimiter = self.CSV_DELIM, quotechar = '"')
			self.reviews = [{'user': review[0], 'rating': review[1], 'raw-text': review[2]} for review in reviews]

		elif self.format_ == 'json':
			reviews = json.load(self.handle)
			self.reviews = [{'user': review['user'], 'rating': review['rating'], 'raw-text': review['raw-text']} for review in reviews]

		elif self.format_ == 'xml':
			#parse XML
			None
		else:
			raise AttributeError

		return self.reviews

	def get_raw_text(self):
		if self.reviews:
			return "".join([review['raw-text'] for review in self.reviews])
