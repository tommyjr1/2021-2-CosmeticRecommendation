import scipy as sp 
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
import surprise

import pickle
import joblib
import re
import dill

#데이터 불러오기
def data_load():
    oydata = pd.read_csv("oydata.csv")
    oydata['id'] = oydata['id'].astype(str)
    iddf = oydata[['id', 'item2', 'point']]
    iddf = iddf.groupby(by=['id', 'item2'], as_index=False).min()
    return iddf

# 테이블을 딕셔너리로 만드는 함수 
def recur_dictify(frame):
    if len(frame.columns) ==1:
        if frame.values.size == 1: return frame.values[0][0]
        return frame.values.squeeze()
    grouped = frame.groupby(frame.columns[0])
    d = {k: recur_dictify(g.iloc[:,1:]) for k,g in grouped}
    return d


# ### 사용자 목록, 화장품 목록을 리스트로 담기
def extract(iddict):
    id_list = []
    cos_set = set()
    for user_key in iddict:
        id_list.append(user_key)
        
        for cos_key in iddict[user_key]:
            cos_set.add(cos_key)

    cos_list = list(cos_set)
    return id_list, cos_list

# ### CF추천시스템에 사용할 딕셔너리 

def create_dic(iddict):
    global id_list
    global cos_list
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
    with open("(모델이름).pkl", 'rb') as f:
        algo = dill.load(f)
    return algo

#모델 수행
def predict(user_id, skin_type, item_type, brand_type):
    global algo
    global id_list
    global cos_list
    reader = surprise.Reader(rating_scale = (1,5))
    col_list = ['id', 'item', 'point']
    cfdata = surprise.Dataset.load_from_df(rddf[col_list], reader)

    who = input('id를 입력해주세요: ')
    print('\n')

    index = id_list.index(who)
    result = algo.get_neighbors(index, k=5)

    print('당신에게 추천드리는 화장품: ', '\n')

    for r1 in result:
        max_rating = cfdata.df[cfdata.df['id']==r1]['point'].max()
        cos_id = cfdata.df[(cfdata.df['point']==max_rating)&(cfdata.df['id']==r1)]['item'][:2/].values
        
        for cos_item in cos_id:
            print(cos_list[cos_item])
    return "대충 결과 반환"


from flask import Flask, request, render_template_string, render_template, url_for
from wtforms import SelectField, SubmitField, StringField


app = Flask(__name__)
app.config["SECRET_KEY"] = "very_secret"

@app.route('/')
def home_page():
    return render_template("homepage.html", title="Home_Page")

@app.route("/resultpage", methods=["POST","GET"])
def result_page():
    if request.method == "POST":
        result = request.form
        
        #입력값 받기(홈페이지 변수명)        
        user_id = result['user_id']
        skin_type = result['skin_type']
        item_type = result['item_type']
        brand_type = result['brand_type']
        
        #함수 실행
        iddf = data_load()
        iddict = recur_dictify(iddf)
        id_list, cos_list = extract(iddict)
        rddf = create_dic(iddict)
        algo = load_model()
        def_result = predict(user_id, skin_type, item_type, brand_type)
        
        return render_template("resultpage.html", title="Result_Page", def_result=def_result)


if __name__ == "__main__":
    app.run()