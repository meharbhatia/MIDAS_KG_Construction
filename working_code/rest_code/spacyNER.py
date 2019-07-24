import spacy
from spacy import displacy
import en_core_web_sm


def getNERs(ex, nlp):
	
	doc = nlp(ex)
	spacyml = [(X, X.ent_iob_, X.ent_type_) for X in doc]

	nstr = ""
	newml = []
	tag = ""
	k=0
	#this loop is only for NER using spacy
	while k<len(spacyml):

		if (spacyml[k][1]=='O' or str(spacyml[k][0]) == "'s"): # To know what is the meaning of 'O' go to https://towardsdatascience.com/named-entity-recognition-with-nltk-and-spacy-8c4a7d88e7da 
			if (len(nstr)>0):
				nn = [ nstr.strip(), tag ] #noun popping from the stack
				newml.append(nn)
				nstr = ""
				tag = ""
		else: # if it is 'B' or 'L' or 'I' or 'U'
			nstr = nstr + str(spacyml[k][0]) + " " #noun stacking (push) is being done
			tag = spacyml[k][2]
			if (k+1 == len(spacyml)):
				nn = [nstr.strip(), tag]
				newml.append(nn)

		k+=1

	return newml


if __name__ == "__main__":

	ex = "Akash Pratap Singh's lawyer appealed to International Court of Trade and Commerce, and in Reserve Bank of India in September and January"
	ex = 'BYD quickly debuted it\'s E-SEED GT concept car and Song Pro SUV alongside it\'s all-new e-series models at the Shanghai International Automobile Industry Exhibition'
	ex ="BYD debuted its E-SEED GT concept car and Song Pro SUV alongside its all-new e-series models at the Shanghai International Automobile Industry Exhibition. The company also showcased its latest Dynasty series of vehicles, which were recently unveiled at the company’s spring product launch in Beijing. A total of 23 new car models were exhibited at the event, held at Shanghai’s National Convention and Exhibition Center, fully demonstrating the BYD New Architecture (BNA) design, the 3rd generation of Dual Mode technology, plus the e-platform framework."
	ex = "The Akash eagerly wanted Mehar Sharma's blue coloured jacket, green umbrella of John Sowa, and Ritwik Mishra's big black red jeans"
	ex = "Akash wants umbrella of Mehar"
	
	nlp = en_core_web_sm.load()
	print(ex)
	for x in getNERs(ex, nlp):
		print(x)