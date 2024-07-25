# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 09:16:42 2024

@author: Alexandre José Ferreira

@licence: MIT

    CSV files must contain a header with the names of 
        the criteria and, respectively, in the rows, ordinal 
        or cardinal numerical information. If in doubt, access
        the example data.csv
    OBS: Each criterion can be a benefit or a cost. However, to specifically 
        analyze dominance and efficiency, increasing numerical order of the 
        criterion results in greater dominance, that is, the higher the value 
        of the criterion the better (benefit maximization).
   
"""

import pandas as pd
from rankability import DataRankable

file=open('data.csv','r')
data1 = pd.read_csv(file)

dr1=DataRankable(data1)
dr1.__rankabilityIndex__()
print('Rankability index:', dr1.rankabilityIndex)
