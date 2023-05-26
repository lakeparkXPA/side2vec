import pandas as pd
from gensim.models import Word2Vec
import pickle

drug_lst = ['IPILIMUMAB','NIVOLUMAB','PEMBROLIZUMAB','DURVALUMAB','AVELUMAB','ATEZOLIZUMAB','CEMIPLIMAB']

node = pd.DataFrame();edge = pd.DataFrame()

# drug_dt 로드
pkl_f = open('/Users/KimJunha/Desktop/side2vec/drug_dt.pkl','rb')
drug_dt = pickle.load(pkl_f)
pkl_f.close()
# drug_ct 로드
pkl_f = open('/Users/KimJunha/Desktop/side2vec/drug_ct.pkl','rb')
drug_ct = pickle.load(pkl_f)
pkl_f.close()

side_ct = {}
for i in drug_lst:
    side_ct[i] = sum(drug_ct[i].values())
    for j in drug_ct[i]:
        if j not in side_ct.keys():
            side_ct[j] = drug_ct[i][j]
        else:
            side_ct[j] = side_ct[j] + drug_ct[i][j]


# 저장했던 모델 로드
model = Word2Vec.load('/Users/KimJunha/Desktop/side2vec/side2vec.model')

# gephi 는 node 와 edge 파일 2가지 필요
node = pd.DataFrame(columns=['id','Label','Category','Price'])
edge = pd.DataFrame(columns=['Source','Target','Type','Weight'])

for i in drug_lst:
    if i not in list(node['Label']):
        node = node.append(pd.Series([len(node)+1, i, 'Drug', round(side_ct[i]/100)],index=['id','Label','Category','Price']),ignore_index=True)

    for j in model.wv.most_similar(positive=[i,'Thyroiditis'],topn=100):
        edge_tmp = []
        if j[0] in drug_dt[i]:
            if j[0] not in list(node['Label']):
                node = node.append(pd.Series([len(node) + 1, j[0], 'SideEffect',side_ct[j[0]]],index=['id','Label','Category', 'Price']),ignore_index=True)

            edge_tmp.append(int(list(node[node['Label'] == i]['id'])[0]))
            edge_tmp.append(int(list(node[node['Label'] == j[0]]['id'])[0]))
            edge_tmp.append('Undirected')
            edge_tmp.append(j[1])
            edge = edge.append(pd.Series(edge_tmp,index=['Source','Target','Type','Weight']),ignore_index=True)

# node, edge 저장
node.to_csv('/Users/KimJunha/Desktop/side2vec/node.csv',index=False)
edge.to_csv('/Users/KimJunha/Desktop/side2vec/edge.csv',index=False)