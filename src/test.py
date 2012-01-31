from Tokenizer import Tokenizer
from ReviewParser import ReviewParser
from POSTagger import POSTagger
import nltk

rev  = ReviewParser(open('../data/reviews/Apple_iPhone_4.csv', 'rb'), 'CSV')
tokenize_patterns = ['[Nn]ikon ?[dD][0-9]+', '([0-9]+ ?mm)', '(auto[ -_]focus)', '(Apple)? ?iphone ?[0-5]?[gs]*']

w = Tokenizer(tokenize_patterns)

rev.parse()

text = rev.get_raw_text()

text = w.tokenize(text)

p = POSTagger(text)

tags = p.nltk_tag()

features = [w.lower() for (w,t) in tags if t.startswith('N') and t != 'NNP']

features = p.stemmer(features)

dist = nltk.FreqDist(features)

obs = [ob for ob in dist.iteritems()]

logfile = open('/tmp/log.txt', 'w')
logfile.write("".join(str(obs)).replace("), (", ")\n("))
logfile.close()
