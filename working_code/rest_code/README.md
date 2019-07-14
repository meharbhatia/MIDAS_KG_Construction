## Updates are here ##

Regarding files (alphabetically):

- ```flairChunking.py``` gives chunks of one sentence using flair library.

- ```clean.py``` cleans the dataset ```icdm_contest_data.csv``` and generates a new clean dataset ```CLEANED_icdm_contest_data.csv```

- ```Coreference.py.ipynb``` is a jupyter notebook file. It creates a dataset with resolved co-references. 

- ```mycorefsample.py``` is a sample file to see co-reference resolution on one sentence.

- ```RuleBased_TripletsExtraction.py``` is outdated version of t2.py 

- ```simpleTripletsStanford.py``` is a sample file to generate simple SVO triplets from simple sentences.

- ```spacyNER+rules.py``` works like t2.py BUT uses spacy NER tool instead of the manual one in t2.py **Currently working on it**

- ```t1.py``` is an old triplet-extracter. It extracts triplets from one sentence

- ```t2.py``` is a pure end-to-end triplet extracter. It uses nltk POS tagger for tagging. It has a function getTriplets which is an updated version of ```t1.py```

- ```t3.py``` works like t2.py only. Just the difference is that it generates ```NN1 | VB | JJ NN2``` triplets whereas t2.py will generate ```NN1 | VB | NN2``` and ```JJ | quality | NN2```

- ```textacy_svo_triplets.py``` Mehar will write on this

- ```textsum.py``` creates a new dataset which also has summaries of news articles. One line and two line summaries. 
