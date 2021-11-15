#!/usr/bin/env python
# coding: utf-8

# In[2]:

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# import scipy
# import math
# import random
# import sklearn
# from sklearn.model_selection import train_test_split
# from sklearn.metrics.pairwise import cosine_similarity

# class FilteringAlgorithm:
def tea_filtering(user_teatype, user_scent, user_effect, user_caff):
    tea_db = (
      pd.read_csv(('apis/lib/assets/Tea DB.csv'), encoding='utf-8')
    )
    df=pd.DataFrame(tea_db)
    def type_filter(teatypes):
        user_typelist=[]
        for teatype in teatypes:
            if teatype in user_teatype:
                user_typelist.append(True)
            else:
                user_typelist.append(False)
        if np.sum(user_typelist)>=1:
            return True
        else:
            return False
    def scent_filter(scents):
        user_scentlist=[]
        for scent in scents:
            if scent in user_scent:
                user_scentlist.append(True)
            else:
                user_scentlist.append(False)
        if np.sum(user_scentlist)>=1:
            return True
        else:
            return False
    def effect_filter(effects):
        user_effectlist=[]
        for effect in effects:
            if effect in user_effect:
                user_effectlist.append(True)
            else:
                user_effectlist.append(False)
        if np.sum(user_effectlist)>=1:
            return True
        else:
            return False
    def caff_filter(caffs):
        user_cafflist=[]
        for caff in caffs:
            if caff == user_caff:
                user_cafflist.append(True)
            else:
                user_cafflist.append(False)
        if np.sum(user_cafflist)>=1:
            return True
        else:
            return False
    df.rename(columns={'맛,향(필터링)':'맛'},inplace=True)
    df.rename(columns={'효능(필터링)':'효능'},inplace=True)
    df.rename(columns={'카페인 여부':'카페인'},inplace=True)
    df.rename(columns={'차 종류':'종류'},inplace=True)
    df.맛.str.split(',')
    df.효능.str.split(',')
    df.종류.str.split('.')
    # df.카페인.apply(caff_filter).sum()
    # df.효능.apply(effect_filter).sum()
    # df.맛.apply(scent_filter).sum()
    # df.종류.apply(type_filter).sum()
    cond_type=df.종류.apply(type_filter)
    cond_effect=df.효능.apply(effect_filter)
    cond_scent=df.맛.apply(scent_filter)
    cond_caff=df.카페인.apply(caff_filter)
    user_finalise=df[cond_type&cond_effect&cond_scent&cond_caff]
    user_finalise
    user_finalise.sort_values(by='재고',axis=0,ascending=False)
    if len(user_finalise)>8:
        user_finalise=user_finalise.sort_values(by='재고',axis=0,ascending=False).head(8) 
    else:
        user_finalise=df[cond_type&cond_scent&cond_caff].sort_values(by='재고',ascending=False).head(8)
        if len(user_finalise)<8:
            user_finalise=df[cond_type&cond_scent].sort_values(by='재고',ascending=False).head(8)
            if len(user_finalise)<8:
                user_finalise=df[cond_type].sort_values(by='재고',ascending=False).head(8)
    user_finalise
    return user_finalise


# %%
