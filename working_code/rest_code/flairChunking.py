#sudo pip3 install flair
from flair.models import SequenceTagger
from flair.data import Sentence
import spacy
import en_core_web_sm
import csv
from nltk import sent_tokenize

		# http://www.surdeanu.info/mihai/teaching/ista555-fall13/readings/PennTreebankConstituents.html
		# SBAR - Clause introduced by a subordinating conjunction.
		# ADJP - Adjective Phrase.
		# ADVP - Adverb Phrase.
		# NP - Noun Phrase. 
		# PP - Prepositional Phrase.
		# QP - Quantifier Phrase (i.e. complex measure/amount phrase); used within NP.
		# VP - Vereb Phrase. 


def getPhrases(ex, tagger):
	ex = ex.strip().strip('.').strip('!').replace('‘','\'').replace('’','\'').replace('“','"').replace('”','"')
	sentence = Sentence(ex)
	tagger.predict(sentence)
	listchunked = sentence.to_tagged_string().split()
	ph = ""
	sentence = []

	k = 0
	while k+1 < len(listchunked):
		if listchunked[k+1] == '<S-NP>' or listchunked[k+1] == '<S-VP>' or listchunked[k+1] == '<S-PP>':
			ph = listchunked[k]
			sentence.append([(ph), (listchunked[k+1][-3:-1])])
			ph = ""
			k+=2
			# print("S")
		elif listchunked[k+1] == '<S-ADJP>':
			ph = listchunked[k]
			sentence.append([(ph), ('NP')])
			ph = ""
			k+=2
		elif listchunked[k+1] == '<S-PRT>':
			ph = listchunked[k]
			sentence.append([(ph), ('PP')])
			ph = ""
			k+=2
		elif listchunked[k+1] == '<B-NP>':
			# ph = ph + listchunked[k]
			while (k+1<len(listchunked) and listchunked[k+1] != '<E-NP>'):
				if not (listchunked[k][0]== '<' and listchunked[k][-1] == '>'):
					ph = ph.strip() + " " + listchunked[k]
				k+=1
			ph = ph.strip() + " " + listchunked[k]
			sentence.append([ph, 'NP'])
			ph = ""
			k+=2
			# print("BNP")
		elif listchunked[k+1] == '<B-VP>':
			while (k+1<len(listchunked) and listchunked[k+1] != '<E-VP>'):
				if not (listchunked[k][0]== '<' and listchunked[k][-1] == '>'):
					ph = ph.strip() + " " + listchunked[k]
				k+=1
			ph = ph.strip() + " " + listchunked[k]
			sentence.append([ph, 'VP'])
			ph = ""
			k+=2
			# print(BVP)
		elif listchunked[k+1] == '<B-ADJP>':
			while (k+1<len(listchunked) and listchunked[k+1] != '<E-ADJP>'):
				if not (listchunked[k][0]== '<' and listchunked[k][-1] == '>'):
					ph = ph.strip() + " " + listchunked[k]
				k+=1
			ph = ph.strip() + " " + listchunked[k]
			sentence.append([ph, 'NP'])
			ph = ""
			k+=2
		elif not ( listchunked[k+1][0] == '<' and listchunked[k+1][-1] == '>' ): #happens with 'CC'
			sentence.append([ listchunked[k] , 'CC'])
			k+=1
		else:
			sentence.append(['REMOVE THIS','XX'])
			k+=2
			# print("here")

	# print("temp chunks")
	# for x in sentence:
	# 	print(x)
	k=0
	while k <len(sentence):
		while (k<len(sentence) and sentence[k][0].find(',')!=-1):
			index = sentence[k][0].find(',')
			if (sentence[k][0][index-1] >= '0' and sentence[k][0][index-1] <= '9' and index+1 < len(sentence[k][0]) and sentence[k][0][index+1] >= '0' and sentence[k][0][index+1] <= '9'):
				break
			ph = list(sentence[k])

			sentence[k][0] = sentence[k][0][:index]

			if (k+1 >= len(sentence)):
				sentence = sentence + [[",","CC"]] + ([[ph[0][index+1:].strip() , ph[1]]] if ph[0][index+1:].strip()!="" else [])
			else:
				sentence = sentence[:k+1] + [[",","CC"]] + ([[ph[0][index+1:].strip() , ph[1]]] if ph[0][index+1:].strip()!="" else []) + sentence[k+1:]
			
			k+=2
		k+=1


	k=0
	while k+1 < len(sentence): #this loop merges consecutive PP like "than/PP in/PP"
		if (sentence[k][1] == "PP" and sentence[k+1][1] == "PP"):
			sentence[k+1][0] = sentence[k][0]+" "+sentence[k+1][0]
			sentence = sentence[:k] + sentence[k+1:]
			k-=1
		elif (sentence[k][1] == "NP" and (sentence[k+1][1] == "NP" or sentence[k+1][0]=="era")):
			sentence[k+1][0] = sentence[k][0]+" "+sentence[k+1][0]
			sentence = sentence[:k] + sentence[k+1:]
			k-=1
		k+=1

	k=0 
	while k<len(sentence):
		if(sentence[k][1]=="NP"):
			if (sentence[k][0].find("and ") == 0):
				sentence[k][0] = sentence[k][0].replace("and ","")
			if ("it's " in sentence[k][0]):
				sentence[k][0] = sentence[k][0].replace("it's ","")
		k+=1
	
	k = 0
	while k<len(sentence):
		if (len(sentence[k][0])==0 or sentence[k][1]=="XX"):
			sentence = sentence[:k] + (sentence[k+1:] if k+1<len(sentence) else [])
		k+=1
		
	if len(sentence)>0 and sentence[-1][1] == "CC":
		sentence = sentence[:-1]
	# k=0
	# while k<len(sentence): #this loop was designed to change possesion tags to "of" PP
	# 	if("'s " in sentence[k][0] and sentence[k][1] == "NP"):
	# 		index = sentence[k][0].find("'s ")
	# 		ph = sentence[k][0]
	# 		sentence[k][0] = sentence[k][0][index+2:].strip()
	# 		ph = ph[:index].strip()
	# 		sentence = sentence[:k+1] +[["of","PP"],[ph,"NP"]] + sentence[k+1:]
	# 	k+=1

	return sentence

def getPhrasesfromfile(iname, aindex, sindex):

	file = open('../../datasets/g050_phrases.csv','r')
	reader = csv.reader(file)
	next(reader)
	tl = []
	for row in reader:
		if (row[0] == iname and int(row[1]) == aindex and int(row[2]) == sindex):
			ttl = []
			ttl.append(row[3])
			ttl.append(row[4])
			tl.append(ttl)
	file.close()
	return tl



if __name__ == "__main__":
	ex = "The company also showcased its latest Dynasty series of vehicles, which were recently unveiled at the company’s spring product launch in Beijing"
	ex = "There are a lot of cars in Los Angeles"
	ex = 'BYD quickly debuted it\'s E-SEED GT concept car and Song Pro SUV alongside it\'s all-new e-series models at the Shanghai International Automobile Industry Exhibition'
	ex = "BYD debuted its E-SEED GT concept car and Song Pro SUV alongside its all-new e-series models at the Shanghai International Automobile Industry Exhibition. The company also showcased its latest Dynasty series of vehicles, which were recently unveiled at the company’s spring product launch in Beijing. A total of 23 new car models were exhibited at the event, held at Shanghai’s National Convention and Exhibition Center, fully demonstrating the BYD New Architecture (BNA) design, the 3rd generation of Dual Mode technology, plus the e-platform framework."
	ex = "The Akash eagerly wanted Mehar Sharma's blue coloured jacket, green umbrella of John Sowa, and Ritwik Mishra's big black red jeans"
	ex = "Akash wants umbrella of Mehar"
	tagger = SequenceTagger.load('chunk')
	print(ex)

	# sentence = Sentence('BYD quickly debuted it\'s E-SEED GT concept car and Song Pro SUV alongside it\'s all-new e-series models at the Shanghai International Automobile Industry Exhibition .')
	for x in getPhrases(ex , tagger):
		print(x)
	# print(type(strchunked))

	input('Enter')

	nlp = en_core_web_sm.load()
	doc = nlp('The company also showcased its latest Dynasty series of vehicles, which were recently unveiled at the company’s spring product launch in Beijing')
	pos_tags = [(i, i.tag_) for i in doc]
	print(pos_tags)


	listchunked = strchunked.split()


	# print(len(listchunked)/2, len(pos_tags))

	print('='*200)

	csvFile = open('../../datasets/g055_Coref_Dataset.csv', 'r')
	reader = csv.reader(csvFile)
	next(reader)
	for row in reader:
		for x in sent_tokenize(row[1]):
			sentence = Sentence(x.strip().strip('.'))
			tagger.predict(sentence)
			print("Actual sentence\n"+x)
			print("Chunked sentence\n"+sentence.to_tagged_string())
			input('\nEnter for next line')

	csvFile.close()
	print(listchunked)

