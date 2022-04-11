import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import seaborn as sns
import random
from pre_process import pre_process,BRAND,CHANNEL,CORD,SEASON
color = sns.color_palette(n_colors=len(BRAND)+1) #sns.light_palette("navy", n_colors=len(BRAND)+1)  #sns.color_palette("cubehelix", n_colors=len(BRAND)+1)
#random.shuffle(color)
COLOR = dict(zip(BRAND,color))
ap_data = pre_process()
"""数据格式形如
{
    'channel':1,
    'sales':{
        {
            'brand':{
                'season1':100,
                'season2':200
            },
            'brand2':{
                's1':300,
                's2':400
            }
        }
    }
} """ 

def remove_zeros(sales:dict)->None:
    """排除sales中的全零项目"""
    for brand,sale_seasons in sales.copy().items():
        flag = True
        for amount in sale_seasons.values(): 
            if amount != 0.0:
                flag = False
        if flag:
            sales.pop(brand)
    return

def sale_brand_season(data:pd.DataFrame,channel_id:int)->dict:
    """获取不同渠道的品牌、季节数据"""
    sale_season = {}
    sale_season['channel'] = CHANNEL[channel_id]
    sales = {}
    for name,loc in data.iterrows():
        if loc['Channel Level 0'] == CHANNEL[channel_id]:
            brand = loc['Brand']
            if sales.get(brand):
                for season in SEASON:
                    sales[brand][season] += loc[f'{season}-income']
            else:
                temp = {}
                for season in SEASON:
                    temp[season] = loc[f'{season}-income']
                sales[brand]= temp.copy()
    remove_zeros(sales) #排除全零项
    sale_season['sales'] = sales
    return sale_season

b2b = sale_brand_season(ap_data,0)
dis = sale_brand_season(ap_data,1)

with open('data_analysis\渠道-季节-品牌销售额\B2B.json','wb+') as f:
    f.write(json.dumps(b2b,indent=4).encode('utf-8'))
with open('data_analysis\渠道-季节-品牌销售额\DIST.json','wb+') as f:
    f.write(json.dumps(dis,indent=4).encode('utf-8'))

#处理并输出单见信息
err = {}
for brand in BRAND:
    if brand not in b2b['sales'].keys():
        if brand not in dis['sales'].keys():
            err[brand] = 'Both'
        else:
            err[brand] = CHANNEL[1]
    else:
        if brand not in dis['sales'].keys():
            err[brand] = CHANNEL[0]
        else:
            pass

with open('data_analysis\渠道-季节-品牌销售额\single-appearance.json','wb+') as f:
    f.write(json.dumps(err,indent=4).encode('utf-8'))

#制图
def pre_cur(sale_season:dict):
    """迭代器，返回初始位置，当前项，颜色"""
    cur  = np.array([0.0 for x in range(9)])
    for brand,sale_season in sale_season.items():
        yield (cur,np.array(list(sale_season.values())),COLOR[brand])
        cur += np.array(list(sale_season.values()))

def plot():
    plt.figure(figsize=(14,14))
    labels= ['2018-4','2019-1','2019-2','2019-3','2019-4','2020-1','2020-2','2020-3','2020-4']
    x = np.arange(len(labels))
    width = 0.3
    for pre,cur,color in pre_cur(b2b['sales']):
        plt.bar(x - (width+0.05)/2,cur,width,bottom=pre,color=color)
    for pre,cur,color in pre_cur(dis['sales']):
        plt.bar(x + (width+0.05)/2,cur,width,bottom=pre,color=color)
    plt.xlabel('Quarter',fontsize=14,labelpad=5)
    plt.ylabel('Sales   / 10 million',fontsize=14,labelpad=5)
    plt.xticks(x,labels=labels)
    #plt.yticks(np.arange(0,53000,step=10000),labels=[1.0,2.0,3.0,4.0,5.0])
    plt.yticks(np.arange(0,30000000,5000000),labels=['0.0','0.5','1.0','1.5','2.0','2.5'])
    plt.title('Sales by quarters',fontsize=20,pad=15)
    #plt.legend()
    plt.savefig(r'data_analysis\渠道-季节-品牌销售额\new.png')
    plt.show()

def plot_b2b():
    plt.figure(figsize=(14,14))
    labels= ['2018-4','2019-1','2019-2','2019-3','2019-4','2020-1','2020-2','2020-3','2020-4']
    x = np.arange(len(labels))
    width = 0.4
    for pre,cur,color in pre_cur(b2b['sales']):
        plt.bar(x,cur,width,bottom=pre,color=color)
    plt.xlabel('Quarter',fontsize=14,labelpad=5)
    plt.ylabel('Sales   / 10 million',fontsize=14,labelpad=5)
    plt.xticks(x,labels=labels)
    plt.yticks(np.arange(0,30000000,5000000),labels=['0.0','0.5','1.0','1.5','2.0','2.5'])
    plt.title(f'Sales by quarters({CHANNEL[0]})',fontsize=20,pad=15)
    #plt.legend()
    plt.savefig(r'data_analysis\渠道-季节-品牌销售额\b2b.png')
    plt.show()

def plot_dis():
    plt.figure(figsize=(14,14))
    labels= ['2018-4','2019-1','2019-2','2019-3','2019-4','2020-1','2020-2','2020-3','2020-4']
    x = np.arange(len(labels))
    width = 0.4
    for pre,cur,color in pre_cur(dis['sales']):
        plt.bar(x,cur,width,bottom=pre,color=color)
    plt.xlabel('Quarter',fontsize=14,labelpad=5)
    plt.ylabel('Sales   / 1 million',fontsize=14,labelpad=5)
    plt.xticks(x,labels=labels)
    plt.yticks(np.arange(0,8000000,1000000),labels=['0.0','1.0','2.0','3.0','4.0','5.0','6.0','7.0'])
    plt.title(f'Sales by quarters({CHANNEL[1]})',fontsize=20,pad=15)
    #plt.legend()
    plt.savefig(r'data_analysis\渠道-季节-品牌销售额\dis.png')
    plt.show()
plot()
#plot_b2b()
#plot_dis()