# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

import scipy as sp 
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
import surprise
import pickle
import joblib
import dill
import os

cwd = os.getcwd()  # Get the current working directory (cwd)
print(cwd)
#데이터 불러오기
def load_data():
    ourdata = pd.read_csv("ourdata.csv")
    ourdata['id'] = ourdata['id'].astype(str)
    iddf = ourdata[['id', 'item2', 'point']]
    iddf = iddf.groupby(by=['id', 'item2'], as_index=False).min()
    return ourdata, iddf

#테이블을 딕셔너리로 만드는 함수
def recur_dictify(frame):
    if len(frame.columns) ==1:
        if frame.values.size == 1: return frame.values[0][0]
        return frame.values.squeeze()
    grouped = frame.groupby(frame.columns[0])
    d = {k: recur_dictify(g.iloc[:,1:]) for k,g in grouped}
    return d

# 사용자 목록, 화장품 목록을 리스트로 담기
def extract(iddict):
    id_list = []
    cos_set = set()
    for user_key in iddict:
        id_list.append(user_key)
        
        for cos_key in iddict[user_key]:
            cos_set.add(cos_key)

    cos_list = list(cos_set)
    return id_list, cos_list

# CF추천시스템에 사용할 딕셔너리 
def create_dic(id_list, cos_list, iddict):
    rating_dic = {
        'id' : [],
        'item' : [],
        'point' : []
    }

    for user_key in iddict:
        for cos_key in iddict[user_key]:
            
            a1 = id_list.index(user_key)
            a2 = cos_list.index(cos_key)
            a3 = iddict[user_key][cos_key]
            
            rating_dic['id'].append(a1)
            rating_dic['item'].append(a2)
            rating_dic['point'].append(a3)

    rddf = pd.DataFrame(rating_dic)
    return rddf

#모델 업로드
def load_model():
    algo = joblib.load("./model/KNN_model.pkl")
    return algo

#id 찾기
def id_func(ourdata):
    #기존회원
    myid = input("id를 입력하세요: ")

    #신규회원
    property_list = list(ourdata['property'].unique())
    subject_list = ['스킨케어', '메이크업', '클렌징', '선케어', '더모 코스메틱']
    brand_list = list(ourdata['item1'].unique())

    print(property_list)
    prop = input("피부타입을 입력하세요: ")
    print('\n')

    print(subject_list)
    sub = input("분야를 선택하세요: ")
    print('\n')

    print(brand_list)
    brand = input("브랜드를 선택하세요: ")
    print('\n')

    if len(myid) == 0:
        newdata = ourdata[ourdata['property'] == prop]
        newdata = newdata[newdata['subject'].str.contains(sub)]

        mydata = newdata[newdata['item1'] == brand]

        if len(mydata) >=1 :
            a = pd.DataFrame(mydata.groupby('id').size())
            a = a.sort_values(by = a.columns[0], ascending = False)
            myid = a.index[0]
        
        else:
            b = pd.DataFrame(newdata.groupby('id').size())
            b = b.sort_values(by = b.columns[0], ascending = False)
            myid = b.index[0]
    return myid

def main_func():
    col_list = ['id', 'item', 'point']
    reader = surprise.Reader(rating_scale = (1,5))
    cfdata = surprise.Dataset.load_from_df(rddf[col_list], reader)
    index = id_list.index(myid)
    result = algo.get_neighbors(index, k=5)

    print('당신에게 추천드리는 화장품: ', '\n')

    for r1 in result:
        max_rating = cfdata.df[cfdata.df['id']==r1]['point'].max()
        cos_id = cfdata.df[(cfdata.df['point']==max_rating)&(cfdata.df['id']==r1)]['item'][:2].values
        
        for cos_item in cos_id:
            print(cos_list[cos_item])
            
            
ourdata, iddf = load_data()
iddict = recur_dictify(iddf)
id_list, cos_list = extract(iddict)
rddf = create_dic(id_list, cos_list, iddict)
algo = load_model()
myid = id_func(ourdata)
main_func()