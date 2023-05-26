# Side2vec

미국 FDA의 약물부작용 데이터 FAERS에서 7가지 표적면역항암제(IPILIMUMAB, NIVOLUMAB, PEMBROLIZUMAB, DURVALUMAB, AVELUMAB,A TEZOLIZUMAB, CEMIPLIMAB)를 Word2vec 모델에 문장의 형태로 input을 하여 약물간 공통적으로 갖고 있는 부작용 탐색


## side2vec_model

Model 은 gensin 의 word2vec을 사용
Input의 형태로 [성별 + 나이 + 임상 상황 + 약물명 + 부작용 + 결과] 형태로 문장으로 묶어서 모델에 적용
약물 별 부작용, 약물 별 부작용 횟수를 pickle 파일로 저장

## side2vec_heatmap

약물 별 부작용 횟수 데이터로 약물간 상관계수 계산을 하여 seaborn 패키지를 이용하여 연도별 heatmap 제작
연도별로 모델 설정을 달리 해서 2010~2019년의 heatmap 변화를 확인 가능

![heatmap](https://github.com/lakeparkXPA/side2vec/assets/47446855/6d143d23-3bdd-4087-aebc-db224886712a)


## sidve2vec_similar

Gephi 의 네트워크 그림을 이용하기 위해 model 에서 생성된 pickle 파일을 이용하여 해당 input 에 맞게 가공
아래와 같은 네트워크 plot 생성
약물 node들과 이어져 있는 공통된 부작용 node 확인 가능

![image](https://github.com/lakeparkXPA/side2vec/assets/47446855/3f64f43b-7fe9-469a-a5f2-7774b44ed028)
