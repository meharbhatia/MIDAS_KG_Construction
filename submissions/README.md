## Updates are here ##

Regarding submissions:

```new_6.csv``` is created by using spacyNER+rulebased , dataset input was cleaned dataset, removed isolated nodes (even with isolated nodes number of tupples were more or less same). Also when the error came, I replaced the new line character (```\n```) with ```<space>```.

```new_7.csv``` has same parameter as that of ```new_6``` just the difference is, it has been run on ```g050_Coref_Dataset.csv```

```new_8.csv``` has same parameter as that of ```new_6``` just the difference is, it has been run on ```g055_Coref_Dataset.csv```

```trial_submission.csv``` includes the triples when redundant triples have been removed from new_7.csv. Triples which do not have (NN, NNS, NNP, CD) in any of the node. Gave a score - 11.78 .

```trial_submission_coref.csv``` includes the triples when redundant triples have been removed from coref_triplets.csv. Triples which do not have (NN, NNS, NNP, CD) in any of the node. Gave a score - 11.82.

