#sudo pip3 install flair
from flair.models import SequenceTagger
from flair.data import Sentence
import spacy
import en_core_web_sm
import csv
from nltk import sent_tokenize




tagger = SequenceTagger.load('chunk')

sentence = Sentence('BYD quickly debuted it\'s E-SEED GT concept car and Song Pro SUV alongside it\'s all-new e-series models at the Shanghai International Automobile Industry Exhibition .')
sentence = Sentence('The company also showcased its latest Dynasty series of vehicles, which were recently unveiled at the company’s spring product launch in Beijing')

tagger.predict(sentence)
strchunked = sentence.to_tagged_string()
print("\n")
print(sentence)
print("\nChunked sentence")
print(strchunked)
# print(type(strchunked))

nlp = en_core_web_sm.load()
doc = nlp('The company also showcased its latest Dynasty series of vehicles, which were recently unveiled at the company’s spring product launch in Beijing')
pos_tags = [(i, i.tag_) for i in doc]
print("\nPOS tags")
print(pos_tags)


listchunked = strchunked.split()
# print(listchunked)
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
	else:
		k+=2
		# print("here")

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

