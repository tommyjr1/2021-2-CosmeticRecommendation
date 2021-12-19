import scipy as sp 
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
import surprise
import pickle
import joblib
import dill

#데이터 불러오기
def load_data():
    ourdata = pd.read_csv("./static/model/ourdata.csv")
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
    algo = joblib.load("./static/model/KNN_model.pkl")
    return algo

#id 찾기
def id_func(ourdata, myid, prop, sub, brand):
    if myid == None:
        newdata = ourdata[ourdata['property'] == prop]
        newdata = newdata[newdata['subject'].str.contains(sub)]

        mydata = newdata[newdata['item1'] == brand]

        if len(mydata) >=1 :
            a = pd.DataFrame(mydata.groupby('id').size())
            a = a.sort_values(by = a.columns[0], ascending = False)
            myid = a.index[0]
        
        else:
            try:
                b = pd.DataFrame(newdata.groupby('id').size())
                b = b.sort_values(by = b.columns[0], ascending = False)
                myid = b.index[0]
            except:
                return 'No'
    return myid

def main_func(id_list, algo, rddf, cos_list, myid, ourdata):
    col_list = ['id', 'item', 'point']
    reader = surprise.Reader(rating_scale = (1,5))
    cfdata = surprise.Dataset.load_from_df(rddf[col_list], reader)
    index = id_list.index(myid)
    neigh = algo.get_neighbors(index, k=5)
    
    branddata = ourdata[['item1', 'item2']].drop_duplicates(['item2'])
    printresult=[]
    for r1 in neigh:
        max_rating = cfdata.df[cfdata.df['id']==r1]['point'].max()
        cos_id = cfdata.df[(cfdata.df['point']==max_rating)&(cfdata.df['id']==r1)]['item'].values
        
        for cos_item in cos_id:
            item = cos_list[cos_item]
            result = branddata[branddata['item2']==item]
            items = [result['item1'].values[0], result['item2'].values[0]]
            printresult.append(items)
    return(printresult)

def get_review(ourdata,product):
    print(product)
    print(ourdata.head())
    tmp = pd.DataFrame()
    tmp = ourdata[ourdata['item2']==product]
    # for i in range(len(ourdata)):
    #     if
    #     tmp = tmp.append(ourdata[ourdata['item2']==product])
    subject = list(tmp['subject'])
    review = list(tmp['review'])
    date = list(tmp['date'])
    result_list = [list([x,y,z]) for x,y,z in zip(subject, review, date)]
    print(tmp.head())
    return(result_list)

from flask import Flask, request, render_template

app = Flask(__name__)
app.config["SECRET_KEY"] = "very_secret"

@app.route('/')
def home_page():
    return render_template("mainPage.html", title="Home_Page")

@app.route("/resultpage", methods=["POST","GET"])
def result_page():
    if request.method == "POST":
        global printresult
        result = request.form
        myid = result.get('user_id')
        prop = result.get('skin_type')
        sub = result.get('item_type')
        brand = result.get('brand_type')

        ourdata, iddf = load_data()
        iddict = recur_dictify(iddf)
        id_list, cos_list = extract(iddict)
        rddf = create_dic(id_list, cos_list, iddict)
        algo = load_model()
        myid = id_func(ourdata, myid, prop, sub, brand)
        if(myid=='No'):
            return {'error':'관련 정보가 부족합니다ㅠㅠ'}
        printresult = main_func(id_list, algo, rddf, cos_list, myid, ourdata)

    return render_template("resultPage.html", title="Result_Page", filter_val = '', printresult=printresult)

# @app.route("/resultFilter")
# def result_page_js():
#     while True:
#         if(len(printresult)!=0):
#             return render_template("resultFilter.js", printresult=printresult)
#             break

@app.route("/reviews", methods=['POST', 'GET'])
def review_list(): 
    if request.method == "POST":
        results = request.form;
        product = results.get('product_name')
        brand = results.get('brand_name')
        filterw = results.get('filter_val')
        print("filter="+filterw)
        ourdata, iddf = load_data()
        review_list = get_review(ourdata, product)
    return render_template("resultPage_review.html", title="reviews", printresult=printresult, brand = brand, product = product, filter_val = filterw ,review_list=review_list)

@app.route("/resultlist", methods=['POST', 'GET'])
def result_list(): 
    if request.method=='POST':
        results = request.form
        filterw = results.get('filter_val')
    return render_template("resultPage.html", title="Result_Page", printresult=printresult, filter_val = filterw)
    
    

if __name__ == "__main__":
    app.run()