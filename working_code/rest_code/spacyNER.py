import spacy
from spacy import displacy
import en_core_web_sm


ex = "Akash Pratap Singh's lawyer appealed to International Court of Trade and Commerce, and in Reserve Bank of India in September and January"

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
	nlp = en_core_web_sm.load()
	print(ex)
	for x in getNERs(ex, nlp):
		print(x)