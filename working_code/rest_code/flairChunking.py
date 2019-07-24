#sudo pip3 install flair
from flair.models import SequenceTagger
from flair.data import Sentence
import spacy
import en_core_web_sm
import csv
from nltk import sent_tokenize

def getPhrases(ex, tagger):
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
		elif not ( listchunked[k+1][0] == '<' and listchunked[k+1][-1] == '>' ): #happens with 'CC'
			sentence.append([ listchunked[k] , 'CC'])
			k+=1
		else:
			k+=2
			# print("here")

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

