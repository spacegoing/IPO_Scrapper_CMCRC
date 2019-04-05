from pymongo import MongoClient
import pandas as pd

client = MongoClient('mongodb://localhost:27017/')
mkt_db = client['IPO']

out_columns = ['date', 'name', 'ric', 'uptick_name']

uptick_name = 'asx'
col = mkt_db[uptick_name]
res = col.find()
res_list = [i for i in res]
res_df = pd.DataFrame(res_list)
out_df = res_df[out_columns]
date_col = out_df['date'].apply(lambda x: x.date())
out_df.loc[:,'date']= date_col
out_df.to_csv('ipo.csv', index=None)
