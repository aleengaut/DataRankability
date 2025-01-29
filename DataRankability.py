# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 09:16:42 2024

@author: Alexandre José Ferreira

@licence: MIT

    CSV files must contain a header with the names of 
the criteria and, respectively, in the rows, ordinal 
or cardinal numerical information + alternatives column with header. 
If in doubt, access the example study1.csv

requirements : numpy, pandas, sklearn
   
"""

import pandas as pd
import rankability

file=open('study3.csv','r')
#file=open('data.csv','r')
#file=open('dataFromKBS.csv','r')


df = pd.read_csv(file)
alt = df['alternatives']
df = df.drop(['alternatives'], axis=1)

dr_1 = rankability.DataRankable(data = df.copy(), alt = alt.copy())
dr_1.__rankabilityIndex__()
dr_1.__sumDominanceVectorAllCriteria__()
print('rankability: ', dr_1.rho)
print('Data:', dr_1.data)

