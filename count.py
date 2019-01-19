import requests
from bs4 import BeautifulSoup
import subprocess
import csv
import re
import pandas as pd
import os



def count(year,month,level,continue_num):
    
    count_lose=0
    count_win=0
    continuous_lose_chance=0
    continuous_win_chance=0

    df=pd.read_csv(f"./data/{year}{month}_{level}.csv")
    rikishi_num=0
    for key, row in df.iterrows():
        #8勝7敗のみ対象
        if row["win"]==8 and row["lose"]==7:
            rikishi_num+=1
            continuous_win=0
            continuous_lose=0
            for winlose in row[3:]:
                #連続敗退中
                if continuous_lose >= continue_num:
                    continuous_lose_chance+=1
                    if winlose == "●":
                        count_lose+=1
                #連続勝利中
                if continuous_win >= continue_num:
                    continuous_win_chance+=1
                    if winlose == "○":
                        count_win+=1


                if winlose == "●":           
                    continuous_lose+=1
                    continuous_win=0
                elif winlose == "○":
                    continuous_win+=1
                    continuous_lose=0
                else:
                    continuous_lose=0
                    continuous_win=0
    #最初のみ
    filename=f"counts_87_{continue_num}.csv"
    if not os.path.exists(filename):
        with open(filename, mode='a') as f:
            writer = csv.writer(f) # 改行コード（\n）を指定しておく
            writer.writerow(["year","month","level","rikishi_num","continuous_lose_chance","count_lose","continuous_win_chance","count_win"]) 
            #f.writelines(["year","month","level","rikishi_num","continuous_lose_chance","count_lose","continuous_win_chance","count_win"])
    
    write_list=[year,month,level,rikishi_num,continuous_lose_chance,count_lose,continuous_win_chance,count_win]
    with open(filename, mode='a') as f:
        writer = csv.writer(f) # 改行コード（\n）を指定しておく
        writer.writerow(write_list)
        #f.writelines(write_list)
    #print(rikishi_num,continuous_lose_chance,count_lose,continuous_win_chance,count_win)
        
if __name__ == "__main__":
    #開催年月リストの作成
    year=["2014","2015","2016","2017","2018"]
    month=["01","03","05","07","09","11"]
    for l in [0,1]:
        for y in year:
            for m in month:
                count(y,m,l,5) #連勝数を指定
