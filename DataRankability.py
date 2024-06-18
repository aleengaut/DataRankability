# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 09:16:42 2024

@author: Alexandre José Ferreira

@licence: MIT

    CSV files must contain a header with the names of 
the criteria and, respectively, in the rows, ordinal 
or cardinal numerical information. If in doubt, access
the example data.csv
   
"""

import pandas as pd
from rankability import datarankable

file=open('data.csv','r')
data1 = pd.read_csv(file)

for columnname in data1.keys():
    try:
        data1[columnname].astype(float)
    except TypeError:
        print('could not convert string to float!')

dr1=datarankable(data1)
print('Rankability index:', dr1.rankabilityIndex())