#!/usr/bin/python

"""
Crawls reviews from various websites.
Supported websites
	Google product search
"""
import urllib2, sys, re, json, string
from BeautifulSoup import BeautifulSoup

class ReviewCrawler:
	def __init__(self, cid, no_reviews = 10):
		self.cid = cid
		self.no_reviews = no_reviews
		self.reviews = []
		self.urls = {
			"gps": "http://www.google.com/products/catalog?cid=$cid&os=reviews&start=$start&rtype=1"
		}

	def validate_filename(self, filename):
		"""
			Filters invalid chars from filenames.
			filename: filename to validate.
		"""
		#Validating filename
		valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
		filename = ''.join(ch for ch in filename if ch in valid_chars)
		return filename.replace(' ', '_')

	def extract_entities(self, soup, n):
		"""
			Extracts review text and other meta data from the review pages.
			soup: The BeautifulSoup object
			n: Number of reviews to parse
		"""
		for i in xrange(0, n):
			review_span = soup.find("span", {'id' : "uc-" + str(i)})
			if review_span is not None:
				review_text = review_span.text
				review_by = review_span.parent.findPreviousSibling("div", {"class": "review-rating"}).text
		#		regex = re.compile('By (.+) ', re.DOTALL)
		#		review_by = regex.search(review_by).group(1).split()[0]
				review_by = review_by.split()[2]
				review_rating = soup.find('div', {'class': 'review-rating'}).findChild().attrMap['title'].split()[0]
				self.reviews.append({'user': review_by, 'rating': review_rating, 'raw-text': review_text})

	def write_reviews(self, reviews, product_name):
		"""
			Write the reviews to a JSON file
			reviews: The reviews to write
			product_name: Name of the JSON file
		"""
		json_file = open("../data/reviews/%s_%s_%s.json" % (self.validate_filename(product_name), str(self.cid), str(len(self.reviews))), "w")
		json_file.write(json.dumps(self.reviews))
		json_file.close()

	def run(self):
		"""
			Main working method of ReviewCrawler
		"""
		start = 0
		num = self.no_reviews
		while start < num:
			url = self.urls['gps'].replace('$cid', self.cid).replace('$start', str(start))
			soup = BeautifulSoup(urllib2.urlopen(url).read(), convertEntities = BeautifulSoup.HTML_ENTITIES)

			if start == 0:
				avail_num = soup.findAll('span', {'class': 'product-num-reviews'})[1].text
				print avail_num, "found"
				avail_num = int(avail_num.split()[0].replace(',', ''))
				if num > avail_num:
					num = avail_num
			self.extract_entities(soup, 10 if num - start > 10 else num - start)
			start += 10
		product_name = soup.find('span', {'class': 'main-title'}).text
		self.write_reviews(self.reviews, product_name)
			
if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Usage: %s <catalog id> [number = 10]" % (sys.argv[0])
		exit()
	try:
		num = int(sys.argv[2])
		if num < 10:
			raise ValueError
	except:
		num = 10
	
	r = ReviewCrawler(sys.argv[1], num)
	r.run()
