## Updates are here ##

Regarding files (alphabetically):

- ```clean.py``` cleans the dataset ```icdm_contest_data.csv``` and generates a new clean dataset ```CLEANED_icdm_contest_data.csv```

- ```Coreference.py.ipynb``` is a jupyter notebook file. It creates a dataset with resolved co-references. 

- ```spacyNER+rules.py``` works like t2.py BUT uses spacy NER tool instead of the manual one in t2.py **Currently working on it**

- ```t2.py``` is a pure end-to-end triplet extracter. It uses nltk POS tagger for tagging. It has a function getTriplets which is an updated version of ```t1.py```
