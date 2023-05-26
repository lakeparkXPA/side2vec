from gensim.models import Word2Vec
import pymssql
import numpy as np
import pandas as pd
import pickle
import os
import json

key_file = os.path.join('', 'key.json')

with open(key_file) as f:
    key = json.loads(f.read())

conn = pymssql.connect(server=key['server'], user=key['user'],
                        password=key['pw'], database=key['database'], port=key['port'])
cur = conn.cursor()

print('SQL Data Loading...')
col = ['demo.primaryid','demo.event_dt', 'th.start_dt','demo.age', 'demo.age_cod', 'demo.sex', 'indi.indi_pt','dr.prod_ai', 're.pt', 'ot.outc_cod']

sql = """select distinct demo.primaryid,demo.EVENT_DT, th.START_DT, demo.age, demo.age_cod, demo.sex, indi.indi_pt, dr.prod_ai, re.pt, ot.OUTC_COD
from dbo.demographic as demo
inner join dbo.drug as dr
on dr.PRIMARYID = demo.PRIMARYID
inner join dbo.reaction as re
on re.PRIMARYID = demo.PRIMARYID
left outer join dbo.outcome as ot
on ot.PRIMARYID = demo.PRIMARYID
left outer join dbo.therapy as th
on th.PRIMARYID = dr.PRIMARYID and th.DSG_DRUG_SEQ = dr.DRUG_SEQ
left outer join dbo.indication as indi
on indi.PRIMARYID = dr.PRIMARYID and indi.INDI_DRIG_SEQ = dr.DRUG_SEQ
where (dr.PROD_AI is not null and (dr.ROLE_COD = 'PS' or dr.ROLE_COD = 'SS'))"""

cur.execute(sql)
data = cur.fetchall()
print('SQL Data Loaded!')

#다루기 쉬원 pandas 형태로 변환
df = pd.DataFrame(data)
df.columns = col

drug_dt = {}
drug_ct = {}
indi_dt = {}

age_cod = {'DEC' : 0.1, 'YR' : 1, 'MON' : 12,'WK' : 52.1429, 'DY' : 365, 'HR' : 8760, None : None}
sex = {'UNK' : 'Unknown', 'M' : 'Male', 'F' : 'Female', None : None}

df = df.replace(np.nan,'')
side_lst = []

print('Transforming To Form...')
for row in df.iterrows():
    tmp = []
    for col in row[1:]:
        # event_dt >= start_dt 인 경우만 추출
        load = 'No'
        if col['demo.event_dt'] == '' or col['th.start_dt'] == '':
            load = 'yes'
        elif int(float(col['demo.event_dt'][:4])) >= float(int(col['th.start_dt'][:4])) and \
                (len(str(int(float(col['demo.event_dt'])))) == 4 or len(str(int(float(col['th.start_dt'])))) == 4):
            load = 'yes'
        elif int(float(col['demo.event_dt'][:6])) >= int(float(col['th.start_dt'][:6])) and \
                (len(str(int(float(col['demo.event_dt'])))) == 6 or len(str(int(float(col['th.start_dt'])))) == 6):
            load = 'yes'
        elif int(float(col['demo.event_dt'][:8])) >= int(float(col['th.start_dt'][:8])):
            load = 'yes'

        if load == 'yes':
            # 나이 연 단위로 변환
            if col['demo.age'] != '':
                age = str(int(float(col['demo.age'])/age_cod[col['demo.age_cod']]))
                tmp.append(age)
            # 성별이 null 인 경우 성별 제외
            if col['demo.sex'] != '':
                sex = col['demo.sex']
                tmp.append(sex)

            # 문장의 형태로 생성
            indi = col['indi.indi_pt']
            drug = col['dr.prod_ai']
            side = col['re.pt']
            out = col['ot.outc_cod']
            tmp = tmp + [indi] + [drug] + [side] + [out]

            #약물에 대한 부작용 딕셔너리
            if col['dr.prod_ai'] in drug_dt.keys():
                if col['re.pt'] not in drug_dt[col['dr.prod_ai']]:
                    drug_dt[col['dr.prod_ai']].append(col['re.pt'])
                    drug_ct[col['dr.prod_ai']].update({col['re.pt']:1})
                else:
                    drug_ct[col['dr.prod_ai']][col['re.pt']] = drug_ct[col['dr.prod_ai']][col['re.pt']] + 1
            else:
                drug_dt[col['dr.prod_ai']] = [col['re.pt']]
                drug_ct[col['dr.prod_ai']] = {col['re.pt']:1}

    side_lst.append(tmp)
print('Transform Complete!')

print('Side2Vec...')
model = Word2Vec(sentences = side_lst,size=200,window=3,min_count=1,workers=4,sg=0,seed=123)
# model 저장
model.save('/Users/KimJunha/Desktop/side2vec/side2vec.model')
# drug 별 SE 저장
f = open('/Users/KimJunha/Desktop/side2vec/drug_dt.pkl','wb')
pickle.dump(drug_dt,f)
f.close()
# drug의 SE count dict 저장
f = open('/Users/KimJunha/Desktop/side2vec/drug_ct.pkl','wb')
pickle.dump(drug_ct,f)
f.close()
print('Side2Vec Done!')