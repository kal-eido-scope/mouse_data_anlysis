from re import L
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt

ap_data = pd.read_excel('Data Analysis Test.xlsx',sheet_name='3;Average Price')
ua_data = pd.read_excel('Data Analysis Test.xlsx',sheet_name='2;Units Adjusted')
BRAND = sorted(set(ap_data['Brand']),key=str.lower)
ITEM_DESCRIPTION = sorted(set(ap_data['Item Description']),key=str.lower)
CHANNEL = ['US B2B Reseller','US Distributor']
CORD = ['Corded','Cordless']
SEASON = [
    "3 Months (Oct'18 - Dec'18)","3 Months (Jan'19 - Mar'19)","3 Months (Apr'19 - Jun'19)",
    "3 Months (Jul'19 - Sep'19)","3 Months (Oct'19 - Dec'19)","3 Months (Jan'20 - Mar'20)",
    "3 Months (Apr'20 - Jun'20)","3 Months (Jul'20 - Sep'20)","3 Months (Oct'20 - Dec'20)"
]
#合并表格
def pre_process():
    for season in SEASON:
        ap_data[f"{season}-ua"] = ua_data[season]
        ap_data[f"{season}-income"] = ap_data[season]*ua_data[season]
    ap_data["income"] = ap_data[[f"{season}-income" for season in SEASON]].sum(axis=1)
    return ap_data