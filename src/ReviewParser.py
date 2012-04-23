#!/usr/bin/python2.7

"""
Parse reviews from all supported formats (JSON, CSV, XML) to a list of dicts
"""
import sys, csv, json
from subprocess import check_output
import settings

class ReviewParser:

	@staticmethod
	def get_available_reviews():
		"""
			Displays a list of all available reviews
		"""
		review_files = check_output(['ls', '-1', settings.reviews_path]).split()
		return review_files

	@staticmethod
	def get_pretty_name(rf):
		"""
			Get the pretty name equivalent of given file
		"""
		return rf.split('-')[0].replace('_', ' ').lower()

	@staticmethod
	def map_cid_to_name(cid):
		"""
			Maps cid (catalogue ID to filenames)
			cid: Catalogue ID
		"""
		review_files = check_output(['ls', '-1', settings.reviews_path]).split()
		for rf in review_files:
			if rf.split('.')[0].split('_')[-2] == cid:
				return rf

	def __init__(self, handle, format_, delimiter = ','):
		"""
			Initilizes the ReviewParser
			handle: file handle
			format_: format of the file
			delimiter: Delimiter to use in case of CSV files
		"""
		self.reviews = []
		self.format_ = format_
		self.handle = handle 
		self.CSV_DELIM = delimiter

	def parse(self):
		"""
			Parse reviews from various file formats to lists
			Supports CSV, JSON and XML(yet to be added) formats
			The list has the following structure:
				[ 
					{
						'user': <reviewer name>,
						'rating': <rating given by the user>,
						'raw-text': <review text>
					},
					{
						'user': <reviewer name>,
						'rating': <rating given by the user>,
						'raw-text': <review text>
					},
					....
				]
		
		"""
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
		"""
			Return raw text from the list of reviews parsed
		"""
		if self.reviews:
			return "".join([review['raw-text'] for review in self.reviews])
