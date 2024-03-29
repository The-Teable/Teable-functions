#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
# import scipy
# import math
import random
# import sklearn
# from sklearn.model_selection import train_test_split
# from sklearn.metrics.pairwise import cosine_similarity
from .ConnectDB import MYSQLDB
# class FilteringAlgorithm:


def tea_filtering(user_teatype, user_scent, user_effect, user_caff):
    myDB = MYSQLDB()
    tea_db = myDB.teas
    df = pd.DataFrame(tea_db)

    def type_filter(teatypes):
        user_typelist = []
        for teatype in teatypes:
            if teatype in user_teatype:
                user_typelist.append(True)
            else:
                user_typelist.append(False)
        if np.sum(user_typelist) >= 1:
            return True
        else:
            return False

    def scent_filter(scents):
        user_scentlist = []
        for scent in scents:
            if scent in user_scent:
                user_scentlist.append(True)
            else:
                user_scentlist.append(False)
        if np.sum(user_scentlist) >= 1:
            return True
        else:
            return False

    def effect_filter(effects):
        user_effectlist = []
        for effect in effects:
            if effect in user_effect:
                user_effectlist.append(True)
            else:
                user_effectlist.append(False)
        if np.sum(user_effectlist) >= 1:
            return True
        else:
            return False

    def caff_filter(caffs):
        user_cafflist = []
        for caff in caffs:
            if caff in user_caff:
                user_cafflist.append(True)
            else:
                user_cafflist.append(False)
        if np.sum(user_cafflist) >= 1:
            return True
        else:
            return False
    # df.rename(columns={'맛,향(필터링)': '맛'}, inplace=True)
    # df.rename(columns={'효능(필터링)': '효능'}, inplace=True)
    # df.rename(columns={'카페인 여부': '카페인'}, inplace=True)
    # df.rename(columns={'차 종류': '종류'}, inplace=True)
    df.rename(columns={'name': 'tea_name'}, inplace=True)
    df.rename(columns={'brand': 'tea_brand'}, inplace=True)
    df.flavor.str.split(',')
    df.efficacies.str.split(',')
    df.type.str.split('.')
    # df.카페인.apply(caff_filter).sum()
    # df.효능.apply(effect_filter).sum()
    # df.맛.apply(scent_filter).sum()
    # df.종류.apply(type_filter).sum()
    cond_type = df.type.apply(type_filter)
    cond_effect = df.efficacies.apply(effect_filter)
    cond_scent = df.flavor.apply(scent_filter)
    cond_caff = df.caffeine.apply(caff_filter)
    user_finalise = df[cond_type & cond_effect & cond_scent & cond_caff]

    if len(user_finalise) > 8:
        # user_finalise = user_finalise.sort_values(
        #     by='재고', axis=0, ascending=False).head(8)
        user_finalise = user_finalise.sample(
            frac=1).reset_index(drop=True).head(8)
    else:
        user_finalise = user_finalise.append(
            df[cond_type & cond_scent & cond_caff]).drop_duplicates(['tea_name'])
        # user_finalise = user_finalise.sort_values(
        #     by='재고', ascending=False).head(8)
        user_finalise = user_finalise.sample(
            frac=1).reset_index(drop=True).head(8)
        if len(user_finalise) < 8:
            user_finalise = user_finalise.append(
                df[cond_type & cond_effect & cond_caff]).drop_duplicates(['tea_name'])
            # user_finalise = user_finalise.sort_values(
            #     by='재고', ascending=False).head(8)
            user_finalise = user_finalise.sample(
                frac=1).reset_index(drop=True).head(8)
            if len(user_finalise) < 8:
                user_finalise = user_finalise.append(
                    df[cond_type & cond_caff]).drop_duplicates(['tea_name'])
                # user_finalise = user_finalise.sort_values(
                #     by='재고', ascending=False).head(8)
                user_finalise = user_finalise.sample(
                    frac=1).reset_index(drop=True).head(8)
                if len(user_finalise) < 8:
                    user_finalise = user_finalise.append(
                        df[cond_type & cond_scent]).drop_duplicates(['tea_name'])
                    # user_finalise = user_finalise.sort_values(
                    #     by='재고', ascending=False).head(8)
                    user_finalise = user_finalise.sample(
                        frac=1).reset_index(drop=True).head(8)
                    if len(user_finalise) < 8:
                        user_finalise = user_finalise.append(
                            df[cond_type & cond_effect]).drop_duplicates(['tea_name'])
                        # user_finalise = user_finalise.sort_values(
                        #     by='재고', ascending=False).head(8)
                        user_finalise = user_finalise.sample(
                            frac=1).reset_index(drop=True).head(8)
                        if len(user_finalise) < 8:
                            user_finalise = user_finalise.append(
                                df[cond_type]).drop_duplicates(['tea_name'])
                            # user_finalise = user_finalise.sort_values(
                            #     by='재고', ascending=False).head(8)
                            user_finalise = user_finalise.sample(
                                frac=1).reset_index(drop=True).head(8)
    return user_finalise
