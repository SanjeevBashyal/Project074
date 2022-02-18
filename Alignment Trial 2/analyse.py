from numpy import float64
from pandas import read_csv
df = read_csv('nag_latlon.csv')
df2=read_csv('outputt.csv')
# print(df['y'],df2['y'])
count=0
# print(df2.index[df2['y']==28.09545609],len(df2['y']))
# print(28.1643218 in list(df2['y']))
count=0
for i in range(len(df['y'])):
    index = df2[(df2['y']==df['y'][i])].index
    print(i,df['y'][i])
    df2.at[index[0],'id2']=int(i)

    if index.any():
        if index[0]<=10755:
            
            df2.at[index[0],'id']=int(i)
            df2.at[index[0],'z']=df.iloc[i,3]
            df2.at[index[0],'fid']=df.iloc[i,0]
            count+=1
print(count)
df2.to_csv('final.csv')
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
#with open('aaa.csv','w',encoding='utf8') as f:
    # for i in range(len(df)):
    #     f.write(df['y'][i].astype(str) +','+df2['y'][i].astype(str))
    #     f.write('\n')  