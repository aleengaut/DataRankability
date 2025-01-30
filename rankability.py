#!/usr/bin/env python3 
# -*- coding: utf-8 -*-

"""
Created on Mon Mar 27 16:10:41 2023
@author: Alexandre José Ferreira
"""

import numpy as np

@staticmethod    
def normalizationDFtoMin0Max1(df):

    for c in df.keys():
        max = df[c].max()
        min = df[c].min()
        delta = max - min
        
        if delta == 0.0: delta = 1.0
        
        df[c] = (df[c] - min*np.ones(df.shape[0])) \
                                /delta              
    return df
       
class DataRankable():
    ''' Class for estimating data rankability using the rho method 
    proposed by Alexandre and Amit.
    
    requirements : numpy
    input: alternative-criteria dataframe WITHOUT alternative column name
        
    OBS: Each criterion can be a benefit or a cost. However, to specifically 
        analyze dominance and efficiency, increasing numerical order of the 
        criterion results in greater dominance, that is, the higher the value 
        of the criterion the better.
    '''
    
    def __init__(self, data = None, alt = None):
        
        for columnname in data.keys():
            try:
                data[columnname].astype(float)
            except TypeError:
                print('could not convert string to float!')
        
        data = normalizationDFtoMin0Max1(data)
        self.data = data
        self.alt = alt
        self.numberOfAlternatives = self.data.shape[0]
        self.numberOfCriteria = self.data.shape[1]
        self.dataOutput = self.data.copy()
        self.dataOutput['alt'] = self.alt
 
    def __rankabilityIndex__(self):
        '''

        Returns
        -------
        rankability_index : rankability index estimation
        '''
        data = np.matrix(self.data)
        rank = np.array(range(self.numberOfAlternatives))
        rank = np.flip(rank)
        
        e = np.zeros(self.numberOfAlternatives)
        for a in range(self.numberOfAlternatives):
            for b in range(self.numberOfAlternatives):
                test = 0
                for c in range(self.numberOfCriteria):
                    if data[a,c] > data[b,c]: test=test+1 
                test = test // self.numberOfCriteria
                e[a] = e[a] + test
        
        rho = e.sum()/rank.sum()
        
        self.rho = round(rho,4)
        self.dataOutput['e'] = e.astype('int64')
    
        return round(rho,2), e
    
    def __completeDominanceVector__(self):
        
        ''' Maximum dominance strength or
        complete dominance set 
                
        Returns
        -------
        completeDominanceVector : minimum non-dominance vector.
        TYPE: array
        '''
        dc = np.array(range(self.numberOfAlternatives))
        dc = np.flip(dc)
        dc = [float(self.numberOfCriteria*dci + 0) for dci in dc]
        self.dc = np.array(dc)
        
        return dc
        
    def __dominanceVector__(self, each_crtrion):
        '''
        Parameters
        ----------
        each_crtrion : criterion.

        Returns
        -------
        dom_each_crtrion : dominance vector for each criterion.
        '''
        d_each_crtrion = np.zeros(self.numberOfAlternatives)
        i=0
        for x in each_crtrion:
            for y in each_crtrion:
                if x>y:
                    d_each_crtrion[i]=d_each_crtrion[i]
                if x<y:
                    d_each_crtrion[i]=d_each_crtrion[i]+1
                i=i+1
            i=0
            
        return d_each_crtrion
    
    def __dominanceEfficiencyVector__(self, each_crtrion):
        '''
        Parameters
        ----------
        each_crtrion : criterion.

        Returns
        -------
        eff_each_crtrion : dominance efficiency vector for each criterion.
        '''
        lambda_each_crtrion = np.zeros(self.numberOfAlternatives)
        i=0
        for x in each_crtrion:
            for y in each_crtrion:
                if x>y:
                    lambda_each_crtrion[i]=lambda_each_crtrion[i]
                if x<y:
                    lambda_each_crtrion[i]=lambda_each_crtrion[i]+y-x
                i=i+1
            i=0
        
        return lambda_each_crtrion
    
    def __sumDominanceVectorAllCriteria__(self):
        '''
        Returns
        -------
        dominanceVectorAllCriteria : dominance vector for all criteria.
        TYPE: array
        '''
        d = np.zeros(self.numberOfAlternatives)
        for each_crtrion in self.data.keys():
        	d = d + self.__dominanceVector__(self.data[each_crtrion])
            
        self.d = d
        self.dataOutput['d'] = d.astype('int64')
        
        return d
    
    def __sumDomEffVectorAllCriteria__(self):
        '''
        Returns
        -------
        dominance_eff_vector : dominance efficiency vector for all criteria.
        '''
        lmbda = np.zeros(self.numberOfAlternatives)
        for each_crtrion in self.data.keys():
        	lmbda = lmbda + self.__dominanceEfficiencyVector__(self.data[each_crtrion])
            
        self.lmbda = np.round(lmbda,4)
        self.dataOutput['lambda'] = np.round(lmbda,4)
        
        return np.round(lmbda,4)
    
    def __dominanceYMatrixik__(self, each_crtrion):
        
        Y=np.zeros((self.numberOfAlternatives, self.numberOfAlternatives), dtype=float)
        i,k=0,0
        for ai in each_crtrion:
            for ak in each_crtrion:
                if ai>ak: 
                    Y[i][k]=Y[i][k]
                if ai<ak: 
                    Y[i][k]=1
                i=i+1
            i=0
            k=k+1
        
        return Y
    
    def __DMatrix__(self):
        '''
        Returns
        -------
        dominance_level : dominance levels where 0 is the Pareto level.
        requirements : run 
                        .__rankabilityIndex__() and 
                        .__sumDomEffVectorAllCriteria__()
            
        '''
        D=np.zeros((self.numberOfAlternatives, self.numberOfAlternatives), dtype=float)
        for each_crtrion in self.data.keys():
        	D = D + self.__dominanceYMatrixik__(self.data[each_crtrion])
        
        self.D = D
        
        return D
