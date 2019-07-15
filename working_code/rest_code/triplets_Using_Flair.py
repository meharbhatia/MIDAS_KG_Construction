#sudo pip3 install flair
from flair.models import SequenceTagger
from flair.data import Sentence
import spacy
import en_core_web_sm
import csv
import nltk
from nltk import sent_tokenize


ex = 'The company also showcased it\'s latest Dynasty series of vehicles, which were recently unveiled at the company\'s spring product launch in Beijing'
ex = 'BYD quickly debuted it\'s E-SEED GT concept car and Song Pro SUV alongside it\'s all-new e-series models at the Shanghai International Automobile Industry Exhibition'
ex = 'Ritwik Mishra\'s lawyer appealed to Reserve Bank Of India to hear the case of Nirav Modi, Mehul Choksy, Rahul Gandhi, Arvind Keriwal and Ramanujam'
ex = "John Sowa from India exhibited at the event, held at Shanghai’s National Convention and Exhibition Center, fully demonstrating the BYD New Architecture (BNA) design, the 3rd generation of Dual Mode technology, plus the e-platform framework"
ex = "An Indian resident, John Sowa, exhibited at the event, held at Shanghai’s National Convention and Exhibition Center, fully demonstrating the BYD New Architecture (BNA) design, the 3rd generation of Dual Mode technology, plus the e-platform framework"
ex = "A total of 23 new car models were exhibited at the event, held at Shanghai’s National Convention and Exhibition Center, fully demonstrating the BYD New Architecture (BNA) design, the 3rd generation of Dual Mode technology, plus the e-platform framework"

tagger = SequenceTagger.load('chunk')

# sentence = Sentence('BYD quickly debuted it\'s E-SEED GT concept car and Song Pro SUV alongside it\'s all-new e-series models at the Shanghai International Automobile Industry Exhibition .')
sentence = Sentence(ex)

tagger.predict(sentence)
strchunked = sentence.to_tagged_string()
print("\n")
print(sentence)
print("\nChunked sentence")
print(strchunked)

nlp = en_core_web_sm.load()
doc = nlp(ex)
# pos_tags = [(i, i.tag_) for i in doc]
pos_tags = nltk.pos_tag(nltk.word_tokenize(ex))
print("\nPOS tags")
print(pos_tags)


listchunked = strchunked.split()
# print(len(listchunked))
# print(len(pos_tags))
print("\n\n")
ph = ""
sentence = []

k = 0
while k < len(listchunked):
	if listchunked[k+1] == '<S-NP>' or listchunked[k+1] == '<S-VP>' or listchunked[k+1] == '<S-PP>':
		ph = listchunked[k]
		sentence.append([(ph), (listchunked[k+1][-3:-1])])
		ph = ""
		k+=2
		# print("S")
	elif listchunked[k+1] == '<B-NP>':
		# ph = ph + listchunked[k]
		while listchunked[k+1] != '<E-NP>':
			ph = ph.strip() + " " + listchunked[k]
			k+=2
		ph = ph.strip() + " " + listchunked[k]
		sentence.append([(ph), (listchunked[k+1][-3:-1])])
		ph = ""
		k+=2
		# print("BNP")
	elif listchunked[k+1] == '<B-VP>':
		while listchunked[k+1] != '<E-VP>':
			ph = ph.strip() + " " + listchunked[k]
			k+=2
		ph = ph.strip() + " " + listchunked[k]
		sentence.append([(ph), (listchunked[k+1][-3:-1])])
		ph = ""
		k+=2
		# print(BVP)
	elif not ( listchunked[k+1][0] == '<' and listchunked[k+1][-1] == '>' ):
		k+=1
	else:
		k+=2
		# print("here")

for x in sentence:
	print(x)

print("\n\n")
k=m=0
while k < len(sentence):
	ph = ""
	for x in nltk.word_tokenize(sentence[k][0]):
		while m < len(pos_tags):
			if (x == pos_tags[m][0]):
				if(pos_tags[m][1]=="RB" or pos_tags[m][1]=="DT" or pos_tags[m][1]==","):
					break
				ph = ph.strip() + " " +x+"^"+pos_tags[m][1]
				m+=1
				break
			m+=1
	sentence[k] = ( ph.strip() , sentence[k][1])
	k+=1

for x in sentence:
	print(x)

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

