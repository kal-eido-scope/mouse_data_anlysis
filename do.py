import pandas as pd
import numpy as np
import json
import matplotlib as mtl
    
ap_data = pd.read_excel('Data Analysis Test.xlsx',sheet_name='3;Average Price')
ua_data = pd.read_excel('Data Analysis Test.xlsx',sheet_name='2;Units Adjusted')
brand_list = sorted(set(ap_data['Brand']),key=str.lower)
item_list = sorted(set(ap_data['Item Description']),key=str.lower)
channel_list = ['US B2B Reseller','US Distributor']
cord_list = ['Corded','Cordless']
season_list = [
    "3 Months (Oct'18 - Dec'18)","3 Months (Jan'19 - Mar'19)","3 Months (Apr'19 - Jun'19)",
    "3 Months (Jul'19 - Sep'19)","3 Months (Oct'19 - Dec'19)","3 Months (Jan'20 - Mar'20)",
    "3 Months (Apr'20 - Jun'20)","3 Months (Jul'20 - Sep'20)","3 Months (Oct'20 - Dec'20)"
]
#合并表格
for season in season_list:
    ap_data[f"{season}-ua"] = ua_data[season]
    ap_data[f"{season}-income"] = ap_data[season]*ua_data[season]
ap_data["income"] = ap_data[[f"{season}-income" for season in season_list]].sum(axis=1)

#先试试不同品牌在不同处分销处的总销售额
"""writer = pd.ExcelWriter(r'try.xlsx')
ap_data.to_excel(writer,sheet_name='all')
writer.save()"""
brand_income_B2B = {}
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
#print(brand_income_B2B)
#print(brand_income_DIS)
"""brand_income = 0
for loc in ap_data.loc:
    income_by_season = """
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
print(np.var(list(new.values())))
print(np.mean(list(new.values())))