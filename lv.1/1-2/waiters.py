import numpy as np
import pandas as pd
import math

from datetime import datetime

class NumRngErr(Exception): # 사용자 정의 에러
    pass

class NotNumErr(Exception):
    pass

def calcpriority(row, max_mile, max_year):
    priority = row.No - row.Mile/max_mile*priority_mile - row.Diff/max_year*priority_year
    return round(priority, 2)

def adddiffdate(df):
    max_mile, max_year = 0, 0
    diffdates = []
    prioritys = []
    for _, row in df.iterrows():
        diffdate = (datetime.now() - datetime.strptime(row.Year, "%Y-%m-%d")).days
        diffdates.append(diffdate)
        # row["Year"] = (datetime.now() - datetime.strptime(row.Year, "%Y-%m-%d")).days
        # df.iloc[idx] = row

        if max_mile < row.Mile:
            max_mile = row.Mile
        if max_year < diffdate:
            max_year = diffdate

    return df.assign(Diff = diffdates), max_mile, max_year

def addpriority(df, max_mile, max_year):
    prioritys = []
    for _, row in df.iterrows():
        prioritys.append(calcpriority(row, max_mile, max_year))
    return df.assign(Prio = prioritys)

def appenduser(df, max_mile, max_year):
    username = input("이름은? ")
    ser = pd.Series(data = [len(df)+1, 0, 0], index=['No','Mile','Diff'])
    df.loc[len(df)] = [len(df)+1, username, 0, 0, datetime.now().strftime("%Y-%m-%d"), calcpriority(ser, max_mile, max_year)]
    # df.append({'No': len(df), 'Name': username, 'Mile': 0, 'Year': 0, 'Diff': 0, 'Prio': calcpriority(ser, max_mile, max_year)}, ignore_index=True)
    return df

def removeuser(df, max_mile, max_year):
    None

def finduser(df, username):
    # 이시방  송진봉
    result = df.loc[df['Name'].str.contains(username)]
    resultlen = len(result)
    print("해당 고객의 검색 결과 : %d명" % (resultlen))
    if resultlen > 1:
        for _, row in result.iterrows():
            print("이름 : %s, 마일리지 : %d, 가입년도 : %s" % (row.Name, row.Mile, row.Year))
    elif resultlen == 1:
        prt = result.iterrows()
        print(prt['Name'], prt['Mile'], prt['Year'])
        None
    else:
        print("해당 데이터 없음")

def switchselection(df, max_mile, max_year):
    print("1. 추가, 2. 삭제, 3. 변경, 4. 검색")
    while True:
        try:
            selection = input("")
            if not selection.isdigit():
                raise NotNumErr
            
            selection = int(selection)
            if selection > 4:
                raise NumRngErr
            if selection < 1:
                raise NumRngErr

            break
        except NotNumErr:
            print("숫자를 입력해주세요.", end=" ")
        except NumRngErr:
            print("범위가 옳지 않습니다.", end=" ")
    
    if selection == 1:
        return appenduser(df, max_mile, max_year), max_mile, max_year
    if selection == 2:

        return df, max_mile, max_year
    if selection == 3:

        return df, max_mile, max_year
    if selection == 4:
        finduser(df, input("인물 검색 >> "))
        return df, max_mile, max_year

df = pd.read_csv('레벨1.3 대기자명단.txt', sep="\t", encoding="cp949")

priority_mile, priority_year = 10, 5

df, max_mile, max_year = adddiffdate(df)
df = addpriority(df, max_mile, max_year)

df_sorted = df.sort_values(by='Mile', ascending=False)
df_sorted = df_sorted.sort_values(by='Prio', ascending=True)

print(datetime.now().strftime("%Y-%m-%d"))

# df, max_mile, max_year = switchselection(df, max_mile, max_year)