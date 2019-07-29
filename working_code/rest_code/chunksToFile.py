from flair.models import SequenceTagger
from flair.data import Sentence
from triplets_using_flair import getTriplets
import spacy
import en_core_web_sm
import csv
import nltk
import re
import time
from statistics import mean 
from nltk import sent_tokenize
from flairChunking import getPhrases


def clearBrackets(article): # to clear the text written inside brackets 
	k=0
	p1 = p2 = 0
	while k<len(article):
		if (article[k]=='('):
			p1 = k
		if (article[k]==')'):
			p2 = k
		if(p1!=0 and p2!=0):
			article = article[:p1]+article[p2+1:].strip()
			p1 = p2 = 0
		k+=1
	article = article.replace('(','').replace('(','')
	return article

tagger = SequenceTagger.load('chunk')
output = [['industry', 'index', 'sentence', 'phrase','category']]
phrases = []
tvar = time.time()
tlist = []
with open('../../datasets/g050_Coref_Dataset.csv', 'r') as csvFile:

	reader = csv.reader(csvFile)
	next(reader) #so that first line is ignored
	k=0
	tlen = 300
	for row in reader:
		article = row[1]
		article = clearBrackets(article)
		sents = sent_tokenize(article)
		s = 0
		while s < len(sents):
			ttl = []
			for x in getPhrases(sents[s], tagger):
				tl = []
				tl.append(row[2])
				tl.append(row[0])
				tl.append(s)
				tl.append(x[0])
				tl.append(x[1])
				ttl.append(tl)
			output+=ttl
			s+=1
		k+=1
		ttaken = round(time.time() - tvar, 2)
		tlist.append(ttaken)
		trem = round(mean(tlist)*300 - mean(tlist)*k, 2)
		print("article "+str(k)+" / "+str(tlen)+"\t\ttime taken: "+str(ttaken)+" sec | Mean time: "+str(round(mean(tlist),2))+" | Time remaining: "+str(trem)+" sec or "+str(round(trem/60,2))+" mins")
		tvar = time.time()
		# if(k==2):
		# 	break
csvFile.close()

# file = open('new_13_withoutJJ_withPosCdExtractor.csv','w')
# for x in output:
# 	print(x)

file = open('../../datasets/g050_phrases.csv','w')
for x in output:
	k=0
	while k<len(x):
		file.write("\"" + str(x[k]).replace("\"","\"\"")+"\"")
		if(k+1 != len(x)):
			file.write(',')
		k+=1

	file.write("\n")
file.close()
