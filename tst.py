
import matplotlib.pyplot as plt
import pandas as pd

dic1 = {'a': [1,2,3], 'b':[4,5,6]}
df1 = pd.DataFrame(dic1)
dic2 = {'b': [1,2,3], 'c':[4,5,6]}
df2 = pd.DataFrame(dic2)

cols1 = df1.columns
cols2 = df2.columns


dfs = [df1, df2]

for df in dfs:
    if 'a' in df.columns:
        continue
    print('is not in')

