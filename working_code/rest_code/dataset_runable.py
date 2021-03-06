#sudo pip3 install flair
from flair.models import SequenceTagger
from flair.data import Sentence
from triplets_using_flair import getTriplets
from reduce_triplets import *
import spacy
import en_core_web_sm
import csv
import nltk
import re
import time
from statistics import mean 
from nltk import sent_tokenize


ex = 'The company also showcased it\'s latest Dynasty series of marvellous vehicles, which were recently unveiled at the company\'s spring product launch in Beijing'
ex = 'BYD quickly debuted it\'s E-SEED GT concept car and Song Pro SUV alongside it\'s all-new e-series models at the Shanghai International Automobile Industry Exhibition'
# ex = 'Ritwik Mishra\'s lawyer appealed to Reserve Bank of India to hear the case of Nirav Modi, Mehul Choksy, Rahul Gandhi, Arvind Keriwal and Ramanujam'
# ex = "John Sowa from India exhibited at the event, held at Shanghai’s National Convention and Exhibition Center, fully demonstrating the BYD New Architecture (BNA) design, the 3rd generation of Dual Mode technology, plus the e-platform framework"
# ex = "An Indian resident, John Sowa, exhibited at the event, held at Shanghai’s National Convention and Exhibition Center, fully demonstrating the BYD New Architecture (BNA) design, the 3rd generation of Dual Mode technology, plus the e-platform framework"
# ex = "A total of 23 new car models were exhibited at the event, held at Shanghai’s National Convention and Exhibition Center, fully demonstrating the BYD New Architecture (BNA) design, the 3rd generation of Dual Mode technology, plus the e-platform framework"
# ex = "John Sowa from India exhibited amazing dancing skills and performed Salsa at the event"
# ex = "\"What is your name?\", asked John"
# ex = "That is the place where John died"
# ex = "The Akash eagerly wanted Mehar Sharma's blue coloured jacket, green umbrella of John Sowa and Ritwik Mishra's red jeans"
# ex = "John went to the market by car, and Mary went to the school"

# tagger = SequenceTagger.load('chunk')


def clearBrackets(article): # to clear the text written inside brackets 
	k=0
	p1 = 0
	p2 = 0
	while k<len(article) and '(' in article:
		if (article[k]=='('):
			p1 = k
		if (article[k]==')'):
			p2 = k
		if(p1!=0 and p2!=0):
			article = article[:p1]+article[p2+1:].strip()
			p1 = 0
			p2 = 0
			k=0
		k+=1
	article = article.replace('(','').replace('(','')
	return article


output = [['industry', 'index', 's1', 'r', 's2']]
show = True
nlp = en_core_web_sm.load()
tvar = time.time()
tlist = []
#change path
with open('../../datasets/g050_Coref_Dataset.csv', 'r') as csvFile:
	reader = csv.reader(csvFile)
	next(reader) #so that first line is ignored
	k=0
	tlen = 300
	for row in reader:
		article = row[1]

		#YOU CAN PUT AN ARTICLE HERE. It'll replace the article you fetched from dataset
		# article = "BYD debuted its E-SEED GT concept car and Song Pro SUV alongside its all-new e-series models at the Shanghai International Automobile Industry Exhibition. The company also showcased its latest Dynasty series of vehicles, which were recently unveiled at the company’s spring product launch in Beijing. A total of 23 new car models were exhibited at the event, held at Shanghai’s National Convention and Exhibition Center, fully demonstrating the BYD New Architecture (BNA) design, the 3rd generation of Dual Mode technology, plus the e-platform framework."
		article = clearBrackets(article)
		triplets = []
		sent = sent_tokenize(article)
		Ngrams = getNgrams(article)
		s = 0
		while s <len(sent):
			# ml = getTriplets(sent[s], tagger)
			ml = getTriplets(row[2], int(row[0]), s, sent[s], Ngrams, show, nlp) #getting triplets for each sentence
			triplets+=ml
			# print("here2")
			if(show):
				input("\n\t\t\tPress ENTER to see next sentence...") #to pause execution
			s+=1
		if(show):
			input("\n\t\tPress ENTER to see next ARTICLE...")


		#at this point triplets variable contains all the triples from the article
		tl = []
		for x in triplets:
			ttl = []
			ttl.append(row[2])
			ttl.append(row[0])
			ttl.append(x[0])
			ttl.append(x[1])
			ttl.append(x[2])
			tl.append(ttl)
		output+=tl

		k+=1
		ttaken = round(time.time() - tvar, 2)
		tlist.append(ttaken)
		trem = round(mean(tlist)*300 - mean(tlist)*k, 2)
		print("article "+str(k)+" / "+str(tlen)+"\t\ttime taken: "+str(ttaken)+" sec | Mean time: "+str(round(mean(tlist),2))+" | Time remaining: "+str(trem)+" sec or "+str(round(trem/60,2))+" mins")
		tvar = time.time()
		# if k==1: #just to see output from top 2 articles
		# 	break

if(show):
	exit()

## to write into a file
file = open('../../submissions/new_13_withoutJJ_withPosCdExtractor.csv','w')
for x in output:
	# k=0
	# while k<len(x):
	# 	file.write(x[k].replace(';','').replace(',','').replace('‘','\'').replace('’','').replace('“','').replace('”','').replace('\"','').replace('\n',' '))
	# 	if(k+1 != len(x)):
	# 		file.write(',')
	# 	k+=1
	
	if( len(x[2])<2 or len(x[4])<2 ):
		continue

	file.write(x[0].replace(';','').replace(',','').replace('‘','\'').replace('’','').replace('“','').replace('”','').replace('\"','').replace('\n',' '))
	file.write(',')
	file.write(x[1].replace(';','').replace(',','').replace('‘','\'').replace('’','').replace('“','').replace('”','').replace('\"','').replace('\n',' '))
	file.write(',')
	file.write(x[2].replace(';','').replace(',','').replace('‘','\'').replace('’','').replace('“','').replace('”','').replace('\"','').replace('\n',' '))
	file.write(',')
	file.write(x[3].replace(';','').replace(',','').replace('‘','\'').replace('’','').replace('“','').replace('”','').replace('\"','').replace('\n',' '))
	file.write(',')
	file.write(x[4].replace(';','').replace(',','').replace('‘','\'').replace('’','').replace('“','').replace('”','').replace('\"','').replace('\n',' '))

	file.write("\n")
file.close()
csvFile.close()


# print(len(listchunked)/2, len(pos_tags))

# print('='*200)

# csvFile = open('../../datasets/g055_Coref_Dataset.csv', 'r')
# reader = csv.reader(csvFile)
# next(reader)
# for row in reader:
# 	for x in sent_tokenize(row[1]):
# 		sentence = Sentence(x.strip().strip('.'))
# 		tagger.predict(sentence)
# 		print("Actual sentence\n"+x)
# 		print("Chunked sentence\n"+sentence.to_tagged_string())
# 		input('\nEnter for next line')

# csvFile.close()
# print(listchunked)

