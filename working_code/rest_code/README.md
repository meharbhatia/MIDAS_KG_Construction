## Updates are here ##

Regarding files (alphabetically):

- ```clean.py``` cleans the dataset ```icdm_contest_data.csv``` and generates a new clean dataset ```CLEANED_icdm_contest_data.csv```

- ```Coreference.py.ipynb``` is a jupyter notebook file. It creates a dataset with resolved co-references. 

- ```chunksToFile.py``` makes chunks of an entire dataset. Stores the chunks in a file. Nmae of the input dataset and name of the output file, both are mentioned in the code.

- ```dataset_runnable.py``` is the file which runs on the entire dataset. Name of that dataset has to be specified in the code. It uses ```triplets_using_flair.py``` to get the triplets and collects them for the entire dataset. 

- ```flairChunking.py``` gives chunks of one sentence using flair library. It has 2 functions. One is used by ```chunkToFile.py```, that function makes chunks from the given sentence using flair library. Second function is used by ```triplets_using_flair.py```, that function reads the chunks stored in the file. File name is specified in the code. Everytime you run the code make sure it is picking up the right ```phrases``` file.

- ```flair extended final triplets.py``` gets JJ-Pos-CD parts of the text. 

- ```jjposcd_extractor.py``` it extracts adjectives (jj), possession tags (pos) and cardinal numbers (cd) from the given phrase of chunker. It also removes these parts and leves behind just the noun part.

- ```main.py``` extracts the triples from OPEN IE in the required submission format. 

- ```mycorefsample.py``` is a sample file to see co-reference resolution on one sentence.

- ```RuleBased_TripletsExtraction.py``` is outdated version of t2.py 

- ```reduce_triplets.py``` under work

- ```refine_using_list.py``` MEHAR UPDATE THIS

- ```removeTrailingComma.py``` as the name suggests. Now it is not required as dataset_runnable file is able to do it by itself. 

- ```simpleTripletsStanford.py``` is a sample file to generate simple SVO triplets from simple sentences.

- ```spacyNER+rules.py``` works like t2.py BUT uses spacy NER tool instead of the manual one in t2.py

- ```spacyNER.py``` gets named entities from the given sentence. Has a function ```getNERs()``` which does this work.

- ```t1.py``` is an old triplet-extracter. It extracts triplets from one sentence

- ```t2.py``` is a pure end-to-end triplet extracter. It uses nltk POS tagger for tagging. It has a function getTriplets which is an updated version of ```t1.py```

- ```t3.py``` works like t2.py only. Just the difference is that it generates ```NN1 | VB | JJ NN2``` triplets whereas t2.py will generate ```NN1 | VB | NN2``` and ```JJ | quality | NN2```

- ```textacy_svo_triplets.py``` MEHAR UPDATE THIS

- ```textsum.py``` creates a new dataset which also has summaries of news articles. One line and two line summaries. 

- ```triplets_flair_chunking_extended.py``` MEHAR UPDATE THIS

- ```triplets_using_flair.py``` with the help of ```flairChunking``` it gets the chunks. Then it creates the triplets from the chunks. Rules are specified in the code. 