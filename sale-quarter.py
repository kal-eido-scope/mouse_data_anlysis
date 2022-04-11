import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
from pre_process import pre_process,BRAND,CHANNEL,CORD,SEASON
ap_data = pre_process()


#先试试不同品牌在不同处分销处的总销售额
"""brand_income_B2B = {}
brand_income_DIS = {}
for name,loc in ap_data.iterrows():
    brand = loc['Brand']
    if loc['Channel Level 0'] == channel_list[0]:
        if brand_income_B2B.get(brand):
            brand_income_B2B[brand] += loc['income']
        else:
            brand_income_B2B[brand] = loc['income']
    else:
        if brand_income_DIS.get(brand):
            brand_income_DIS[brand] += loc['income']
        else:
            brand_income_DIS[brand] = loc['income']

new = {}
err_dict = {}
for key in brand_income_B2B.keys():
    if brand_income_B2B[key]:
        if brand_income_DIS.get(key):
            new[key]=brand_income_DIS[key]/brand_income_B2B[key]
        else:
            err_dict[key] = channel_list[0]
    else:
        err_dict[key] = channel_list[1]
with open('data_analysis\渠道-品牌销售额\B2B.json','wb+') as f:
    f.write(json.dumps(brand_income_B2B).encode('utf-8'))
with open('data_analysis\渠道-品牌销售额\DIST.json','wb+') as f:
    f.write(json.dumps(brand_income_B2B).encode('utf-8'))
with open('data_analysis\渠道-品牌销售额\DIS-B2B%.json','wb+') as f:
    f.write(json.dumps(new).encode('utf-8'))
with open('data_analysis\渠道-品牌销售额\single-appearance.json','wb+') as f:
    f.write(json.dumps(err_dict).encode('utf-8'))

#print(np.var(list(new.values())))
#print(np.mean(list(new.values())))"""

#尝试不同分销商不同季度的变化
def channel_season(data:pd.DataFrame,key:int):
    """0 for b2b, 1 for distribution"""
    income_seasons = {}
    for name,loc in data.iterrows():
        if loc['Channel Level 0'] == CHANNEL[key]:
            for season in SEASON:
                if income_seasons.get(season):
                    income_seasons[season] += loc[f'{season}-income']
                else:
                    income_seasons[season] = loc[f'{season}-income']
    return income_seasons
b2b = channel_season(ap_data,0)
dis = channel_season(ap_data,1)
with open('data_analysis\渠道-季节销售额\B2B.json','wb+') as f:
    f.write(json.dumps(b2b,indent=4).encode('utf-8'))
with open('data_analysis\渠道-季节销售额\DIST.json','wb+') as f:
    f.write(json.dumps(dis,indent=4).encode('utf-8'))

#np.array(b2b.values)
plt.figure(figsize=(10,8),dpi=100)
labels= ['2018-4','2019-1','2019-2','2019-3','2019-4','2020-1','2020-2','2020-3','2020-4']
x = np.arange(len(labels))
width = 0.4
plt.bar(x - width/2,b2b.values(),width,label=CHANNEL[0])
plt.bar(x + width/2,dis.values(),width,label=CHANNEL[1])
plt.xlabel('Quarter',fontsize=14,labelpad=5)
plt.ylabel('Sales / 10 million',fontsize=14,labelpad=5)
plt.xticks(x,labels=labels)
plt.yticks(np.arange(0,30000000,5000000),labels=['0.0','0.5','1.0','1.5','2.0','2.5'])
plt.title('Sales by quarters',fontsize=20,pad=15)
plt.legend()
plt.savefig(r'data_analysis\渠道-季节销售额\result.png')
plt.show()