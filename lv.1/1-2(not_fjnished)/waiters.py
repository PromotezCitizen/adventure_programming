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
    username = input("인물 검색 >> ")
    result = df.loc[df['Name'].str.contains(username)]
    resultlen = len(result)
    sav_mile, sav_year = max_mile, max_year
    max_mile, max_year = 0, 0
    print("해당 고객의 검색 결과 : %d명" % (resultlen))
    sav_mile, sav_year = max_mile, max_year
    if resultlen == 1:
        
        test = df.drop(result.No-1)
        print(result.iloc[0].No)
        # for idx, row in test.iterrows():
        #     if row.No > result.No - 1:
        #         row.No = row.No - 1
        #     if max_mile < row.Mile: max_mile = row.Mile
        #     if max_year < row.Diff: max_year = row.Diff
        #     #print("이름 : %s, 마일리지 : %d, 가입년도 : %s" % (row.Name, row.Mile, row.Year))

        print(test)
        if (max_mile == sav_mile) and (max_year == sav_year):
            None
        
    elif resultlen > 1:
        print("해당 이름을 가진 회원은 아래와 같습니다")
        for _, row in result.iterrows():
            print("이름 : %s, 마일리지 : %d, 가입년도 : %s" % (row.Name, row.Mile, row.Year))
        
        while True:
            idx = int(input("몇 번째 회원을 삭제하겠습니까(%d~%d) >> " % (1, resultlen))) - 1

            try:
                if idx > resultlen-1:
                    raise NumRngErr
            except NumRngErr:
                print("옳지 않은 범위입니다. 다시 입력해주세요.", sep=" ")
                continue
            rowidx = result.iloc[idx].No
            print(result.loc[rowidx-1])
            if input("해당 회원이 맞습니까(T/F)? ").upper() == "T":
                df = df.drop([rowidx-1])
                for _, row in df.iterrows():
                    if row.No > rowidx:     row.No = row.No - 1
                    if max_mile < row.Mile: max_mile = row.Mile
                    if max_year < row.Diff: max_year = row.Diff
                    
                print(df)
                if (max_mile == sav_mile) and (max_year == sav_year):
                    break

                # for idx, row in df.iterrows():
                #     df.iloc[[idx], ['No', 'Prio']] = [No, calcpriority(row, max_mile, max_year)]
                
                break
            print("다시 선택해주세요.", sep=" ")
    else:
        print("해당 데이터 없음")


    return df, max_mile, max_year

def finduser(df):
    username = input("인물 검색 >> ")
    result = df.loc[df['Name'].str.contains(username)]
    resultlen = len(result)
    print("해당 고객의 검색 결과 : %d명" % (resultlen))
    if resultlen == 1:
        prt = result.iterrows()
        print(prt['Name'], prt['Mile'], prt['Year'])
        return
    if resultlen > 1:
        for _, row in result.iterrows():
            print("이름 : %s, 마일리지 : %d, 가입년도 : %s" % (row.Name, row.Mile, row.Year))
        return
    else:
        print("해당 데이터 없음")
        return

def saveuser(df):
    df[["No", "Name", "Mile", "Year"]].to_csv("test.txt", sep="\t", encoding="cp949", index=None)
    return True

def inputnum():
    while True:
        try:
            selection = input("1. 추가, 2. 삭제, 3. 변경, 4. 검색, 5. 종료")
            if not selection.isdigit():
                raise NotNumErr
            
            selection = int(selection)
            if selection > 5:
                raise NumRngErr
            if selection < 1:
                raise NumRngErr

            return selection
        except NotNumErr:
            print("숫자를 입력해주세요.", end=" ")
        except NumRngErr:
            print("범위가 옳지 않습니다.", end=" ")

def switchselection(df, max_mile, max_year):
    exit_flag = False
    selection = inputnum()

    if selection == 1: # append
        df = appenduser(df, max_mile, max_year)
    if selection == 2: # delete
        print(max_mile, max_year)
        df, max_mile, max_year = removeuser(df, max_mile, max_year)
        print(max_mile, max_year)
        None
    if selection == 3: # modify
        moduser = None
        None
    if selection == 4: # search
        finduser(df)
    if selection == 5: # exit
        exit_flag = saveuser(df)
        
    return df, max_mile, max_year, exit_flag

def appdf():
    df = pd.read_csv('test.txt', sep="\t", encoding="cp949")

    df, max_mile, max_year = adddiffdate(df)
    df = addpriority(df, max_mile, max_year)
    return df, max_mile, max_year

# 레벨1.3 대기자명단.txt
priority_mile, priority_year = 10, 5

df, max_mile, max_year = appdf()

df_sorted = df.sort_values(by='Mile', ascending=False)
df_sorted = df_sorted.sort_values(by='Prio', ascending=True)

exit_flag = False
while not exit_flag:
  df, max_mile, max_year, exit_flag = switchselection(df, max_mile, max_year)