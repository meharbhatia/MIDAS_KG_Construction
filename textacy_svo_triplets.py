'''
To import textacy, either use pip install textacy 
or 
download the source tar.gz rom https://pypi.org/project/textacy/
'''

import textacy

text1 = nlp(u'Norway has a lot of electric cars, so many that it can make anyone driving a new vehicle with an internal combustion engine look like a Luddite.')
text_ext1 = textacy.extract.subject_verb_object_triples(text1)
a1 = list(text_ext1)
print(a1)

'''
[(Norway, has, lot), (anyone, driving, vehicle)]
'''