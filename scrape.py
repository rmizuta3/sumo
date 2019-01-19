import requests
from bs4 import BeautifulSoup
import subprocess
import csv
import re
import pandas as pd

def get_table(year,month):
    s = requests.Session()
    r = s.get(f'https://sports.yahoo.co.jp/sumo/torikumi/hoshitori/?bashoId={year}{month}')
    soup = BeautifulSoup(r.text, "lxml")

    #テーブルを指定
    tables = soup.findAll("table",{"class":"w100 hoshitori_list f_gray02"})#[0]

    for level, table in enumerate(tables):
        rows = table.findAll("tr")

        name=[]
        wincount=[]
        losecount=[]
        results=[]
        for row in rows:
            result=[]
            for cell in row.findAll(['td', 'th']):
                text = cell.get_text()

                #力士名、勝敗数の取得
                if "★" in text or "☆" in text:
                    #rikishi.append(text)
                    t1=text.rsplit("勝",1) #名前に勝が入っている力士がいる
                    t2=t1[1].rsplit("敗",1)
                    #数字を除外
                    name.append(re.sub(r'\d', '', t1[0]).split(" ")[1])
                    #数字以外を除外
                    wincount.append(re.sub(r'\D', '', t1[0]))
                    losecount.append(re.sub(r'\D', '', t2[0]))

                #日付毎の勝敗を取得
                for mark in ["や","○","●","□","■"]:        
                    if mark in text:
                        result.append(mark)
                        #print(text.split(mark)[0])

                if re.sub(r'\D', '', text) == "15" and len(result)>0: 
                #if text.split(mark)[0]=="15": 
                    while len(result) < 15: #元の表の欠損対応
                        result.append("?")
                        
                    results.append(result)
                    result=[]

        #出力作成    
        df=pd.DataFrame()
        df["name"]=name
        df["win"]=wincount
        df["lose"]=losecount
        resultdf=pd.DataFrame(results)
        resultdf.columns=[i+1 for i in range(15)]
        df=pd.concat([df,resultdf],axis=1)
        df.to_csv(f"./data/{year}{month}_{level}.csv",index=False)


if __name__ == "__main__":
    #開催年月リストの作成
    year=["2014","2015","2016","2017","2018"]
    month=["01","03","05","07","09","11"]
    for y in year:
        for m in month:
            get_table(y,m)