#!/usr/bin/env python3 
# -*- coding: utf-8 -*-

"""
Created on Mon Mar 27 16:10:41 2023

@author: Alexandre José Ferreira
"""


#import os
import numpy as np
from numpy.linalg import norm
       
class datarankable:
    
    def __init__(self, df1):
        self.data = df1.to_numpy()   
        self.data = np.matrix(self.data).transpose()
        self.xrown = self.data.shape[1]
        self.yrown = self.data.shape[0]
    
    def __dmin__(self): #obj.__dmin_()
        x = np.array(range(self.xrown))
        x = np.flip(x)
        i=0
        x = [self.yrown*xi+i for xi in x] #dmin
        x = [float(xi) for xi in x]
        self.dmin = np.array(x)
        
        return self.dmin
        
    def __dmax__(self): #obj.__dmax_()
        self.dmax = np.ones(self.xrown)*self.__dmin__().sum()/self.xrown
        
        return self.dmax

    def __dominance__(self, vec):
        dom=np.zeros(len(vec))
        i=0;
        for x in vec:
            for y in vec:
                if x>y: #=
                    dom[i]=dom[i]; #OR don[i]=don[i]+x-y;
                if x<y: #=
                    dom[i]=dom[i]+1; #OR don[i]=don[i]+y-x;
                i=i+1;
            i=0;
            
        return dom
    
    def __multidom__(self):
        data = self.data.transpose()
        dom = np.zeros(self.xrown)
        for col in range(self.yrown):
        	dom = dom + self.__dominance__(data[:,col])
        
        dom = np.sort(dom)
        dom = np.flip(dom)
        if not dom.any(): dom=self.__dmax__()
        self.dom = dom
        
        return self.dom
    
    def rankabilityIndex(self):
        a=self.__dmin__()
        b=self.__dmax__()
        c=self.__multidom__()
        cos_sim_1 = np.dot(a, b)/(norm(a)*norm(b))
        cos_sim_2 = np.dot(c, a)/(norm(c)*norm(a)) #x
        rankability = np.abs(cos_sim_2 - cos_sim_1)/(1.0-cos_sim_1)
        self.rankability = rankability
    
        return self.rankability
    
    def __domlevel__(self):
        # caso m << n e m >=2
        level=0 # nivel de dominancia...faixa pareto
        vec=[]
        dom = self.__multidom__()
        m = self.yrown 
        for i in dom:
            for j in dom:
                if i-j >= m:
                    level+=1
                    
            vec.append(level)
            level=0
            
        #vec = vec-vec[0]*np.ones(len(vec))
        self.domlevel = vec
        
        return self.domlevel
