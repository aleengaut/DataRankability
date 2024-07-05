# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 09:16:42 2024

@author: Alexandre José Ferreira

@licence: MIT

    CSV files must contain a header with the names of 
the criteria and, respectively, in the rows, ordinal 
or cardinal numerical information. If in doubt, access
the example data.csv

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
