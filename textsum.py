# -*- coding: utf-8 -*-
# https://github.com/miso-belica/sumy

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import csv


LANGUAGE = "english"
SENTENCES_COUNT = 2


# if __name__ == "__main__":
    # url = "https://en.wikipedia.org/wiki/Automatic_summarization"
    # parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
    # or for plain text files
# parser = PlaintextParser.from_file("document.txt", Tokenizer(LANGUAGE))
# stemmer = Stemmer(LANGUAGE)

# print(parser)
# input()
# summarizer = Summarizer(stemmer)
# summarizer.stop_words = get_stop_words(LANGUAGE)

# for sentence in summarizer(parser.document, SENTENCES_COUNT):
#     print(sentence)

output = [['index', 'content', 'industry', '1linecontent', '2linecontent']]
#change path
with open('icdm_contest_data.csv', 'r') as csvFile:
	reader = csv.reader(csvFile)
	next(reader)
	for row in reader:
		file = open("document.txt",'w')
		file.write(row[1])
		file.close()
		parser = PlaintextParser.from_file("document.txt", Tokenizer(LANGUAGE))
		stemmer = Stemmer(LANGUAGE)
		summarizer = Summarizer(stemmer)
		summarizer.stop_words = get_stop_words(LANGUAGE)
		str1 = ""
		str2 = ""
		tl = []
		for sentence in summarizer(parser.document, 1):
			str1 = str1.strip() + " " + str(sentence)
		
		for sentence in summarizer(parser.document, 2):
			str2 = str2.strip() + " " + str(sentence)
		tl.append(row[0])
		tl.append(row[1])
		tl.append(row[2])
		tl.append(str1)
		tl.append(str2)
		output.append(tl)
		# print(output[-1])
		# input()

file = open('SUMM_icdm_contest_data.csv','w')
for x in output:
	for y in x:
		file.write('"'+y.replace('"','""')+'"'+',')
	file.write("\n")
file.close()
csvFile.close()


