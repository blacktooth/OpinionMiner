from ReviewParser import ReviewParser
from FeatureExtractor import FeatureExtractor

review_file = ['Apple_iPhone_4.csv', 'Blackberry_Torch_9800.csv', 'Nikon_D90.csv', 'Canon_ELPH_300_HS.csv']
rev = ReviewParser(open('../data/reviews/' + review_file[3], 'rb',), 'CSV')

rev.parse()

text = rev.get_raw_text()

f = FeatureExtractor(text)

print f.get_frequent_features(5)

"""
#tokenize_patterns = ['[Nn]ikon ?[dD][0-9]+', '([0-9]+ ?mm)', '(auto[ -_]?focus)', '(Apple)[ ]?(iphone)??[0-5]?[gs]*']
features = [w.lower() for (w,t) in tags if t.startswith('N') and t != 'NNP']

features = p.stemmer(features)

dist = nltk.FreqDist(features)

obs = [ob for ob in dist.iteritems()]

logfile = open('/tmp/log.txt', 'w')
logfile.write("".join(str(obs)).replace("), (", ")\n("))
logfile.close()
"""
