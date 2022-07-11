import numpy as np
import pandas as pd
import math

from datetime import datetime

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
        priority = row.No - row.Mile/max_mile*priority_mile - row.Diff/max_year*priority_year
        priority = round(priority, 2)
        prioritys.append(priority)
    return df.assign(Prio = prioritys)

df = pd.read_csv('레벨1.3 대기자명단.txt', sep="\t", encoding="cp949")

priority_mile, priority_year = 10, 5

df, max_mile, max_year = adddiffdate(df)
df = addpriority(df, max_mile, max_year)

df_sorted = df.sort_values(by='Mile', ascending=False)
df_sorted = df_sorted.sort_values(by='Prio', ascending=True)

