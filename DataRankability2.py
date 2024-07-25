# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 09:16:42 2024

@author: Alexandre José Ferreira

@licence: MIT

   CSV files must contain a header with the names of 
   the criteria and, respectively, in the rows, ordinal 
   or cardinal numerical information + alternatives column with header. 
   If in doubt, access the example study1.csv

    OBS: Each criterion can be a benefit or a cost. However, to specifically 
        analyze dominance and efficiency, increasing numerical order of the 
        criterion results in greater dominance, that is, the higher the value 
        of the criterion the better (benefit maximization).

requirements : numpy, pandas, sklearn
   
"""

import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
import rankability

file=open('study3.csv','r')
df = pd.read_csv(file)
alt = df['alternatives']
df = df.drop(['alternatives'], axis=1)

'''
PCA must be applied carefully. It should be applied when the \
    rankability of the data is very low and if it is lower than \
        the rankability of the PCs.
'''
#pca = PCA(n_components=2)
#pca.fit(df.to_numpy())
#print(pca.explained_variance_ratio_)
#print(pca.singular_values_)

#df = pd.DataFrame(pca.fit_transform(df), columns=['pc1', 'pc2'])

dr_1 = rankability.DataRankable(df = df, dfalt = alt)
dr_1.__rankabilityIndex__()
dr_1.__sumDomEffVectorAllCriteria__()
dr_1.__dominanceLevelVector__()
print('Rankability index:', dr_1.rankabilityIndex)
print('Data:', dr_1.df)
