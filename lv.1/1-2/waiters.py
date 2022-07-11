import numpy as np
import pandas as pd

df = pd.read_csv('레벨1.3 대기자명단.txt', sep="\t", encoding="cp949")
print(df['Name'])