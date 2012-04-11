import json, web
from OpinionMiner import *
import settings

app = web.application(settings.urls, globals())

"""
	Format for data exchange
	{
		'features': [
			'ftr1': {
				'word': <string>, 
				'no_postive': <integer>, 
				'no_negative': <integer>, 
				'neutral': <integer>, 
				'best_sentence': <text>
			},
			'ftr2': {
				'word': ftr_word,
				.....
				.....
			},
			......
			......

		],
		
		'no_reviews': <integer>
	}
	
	Format for products data exchange:
	{
		'products': [
			'prd1': {
				'word': <string>,
				'cid': <string>,
				'nuumber': <int>,
			},
			.....
			.....

		]
	}
	Requests to accept:
		http://host:<port>/summarize?cid=<cid>&min_support=<min_sup>
		http://host:<port>/getproducts
"""

class Products:
	def GET(self):
		review_files = ReviewParser.get_available_reviews()
		prd_json = {}
		prd_json['products'] = []
		for rf in review_files:
			entity = {}
			entity['name'] = rf
			entity['cid'] = rf.split(".")[0].split("_")[-2]
			entity['number'] = rf.split(".")[0].split("_")[-1]
			prd_json['products'].append(entity)
	
		return json.dumps(prd_json)
		
class OpinionSummarizer:
	def GET(self):
		return None

if __name__ == "__main__":
	app.run()
