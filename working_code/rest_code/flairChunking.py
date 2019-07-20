#sudo pip3 install flair
from flair.models import SequenceTagger
from flair.data import Sentence
import spacy
import en_core_web_sm
import csv
from nltk import sent_tokenize



ex = "The company also showcased its latest Dynasty series of vehicles, which were recently unveiled at the company’s spring product launch in Beijing"
ex = "There are a lot of cars in Los Angeles"
tagger = SequenceTagger.load('chunk')

# sentence = Sentence('BYD quickly debuted it\'s E-SEED GT concept car and Song Pro SUV alongside it\'s all-new e-series models at the Shanghai International Automobile Industry Exhibition .')
sentence = Sentence(ex)

tagger.predict(sentence)
strchunked = sentence.to_tagged_string()
print(strchunked)
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

