import spacy
import neuralcoref
nlp = spacy.load('en')
neuralcoref.add_to_pipe(nlp, greedyness=0.55) #0.55 is best value I've seen

str1 = u"Norway has a lot of electric cars, so many that it can make anyone driving a new vehicle with an internal combustion engine look like a Luddite. Mercedes-Benz brought us there to experience the EQC, and possibly to normalize it in a sea of EVs that makes California look like a land of late adopters. Outside Oslo, where cars were larger and more upscale than in other parts of Europe, and Tesla vehicles (S and X) are a more common sight than around Los Angeles or the Bay Area, the EQC fit right in. DON'T MISS: Mercedes-Benz EQC Edition 1886 electric SUV kicks off a new era \
After a couple of rain-soaked days driving the EQC there last week, we can say that it will be a great addition in the U.S. when it arrives sometime in 2020. At about 187 inches long, the EQC400 4Matic crossover splices into the American mid-sizers."
doc = nlp(str1)
# doc = nlp(u'John went to Norway and it was beautiful.')

print(doc._.coref_clusters)
print(doc._.coref_clusters[0].mentions)
print(str1)
print(doc._.coref_resolved)