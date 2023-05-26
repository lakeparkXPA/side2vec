import pandas as pd
import numpy as np
import pickle

import seaborn as sns
import matplotlib.pyplot as plt

# drug_ct 로드
pkl_f = open('/Users/KimJunha/Desktop/side2vec/drug_ct_2014.pkl','rb')
drug_ct = pickle.load(pkl_f)
pkl_f.close()

drug_lst = ['IPILIMUMAB','NIVOLUMAB','PEMBROLIZUMAB','DURVALUMAB','AVELUMAB','ATEZOLIZUMAB','CEMIPLIMAB']

immune_ct = pd.DataFrame(columns=['Drug','SideEffect','Count','Ratio'])
drug=[];sideeffect=[];ratio=[];#count=[]

# drug 대 side effect 테이블 생성
for i in drug_lst:
    for j in drug_ct[i]:
        drug.append(i)
        sideeffect.append(j)
        #count.append(drug_ct[i][j])
        ratio.append(drug_ct[i][j] / sum(drug_ct[i].values()))

immune_ct['Drug'] = drug; immune_ct['SideEffect']=sideeffect; immune_ct['Ratio'] = ratio;# immune_ct['Count']=count

#heat_count = immune_ct.pivot('SideEffect', 'Drug', 'Count').replace(np.nan,0)
heat_ratio = immune_ct.pivot('SideEffect', 'Drug', 'Ratio').replace(np.nan,0)

# 약물간의 상관계수 계산 및 테이블화
heat_corr = pd.DataFrame(columns=['Drug1','Drug2','Corr'])
drug1 = [];drug2 = [];corr = []

for i in drug_lst:
    for j in drug_lst:
        drug1.append(i)
        drug2.append(j)
        corr.append(heat_ratio[i].corr(heat_ratio[j]))
heat_corr['Drug1'] = drug1; heat_corr['Drug2'] = drug2; heat_corr['Corr'] = corr

drug_corr = heat_corr.pivot('Drug1','Drug2','Corr')

# heatmap 그래프 생성 annot(박스안 수 표시), cmap(색상지정)
sns.heatmap(drug_corr,annot=True, cmap='RdYlGn_r')
plt.title('Correlation Between Two Drugs')
fig = plt.gcf()
plt.show()
fig.savefig('/Users/KimJunha/Desktop/side2vec/heatmap2014.png')