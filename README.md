# Recipes-recommender

[Dataset](https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions/data?select=RAW_interactions.csv)


1. 전처리
    1. 결측치 처리
    2. 이상치 처리
    3. 데이터 분포 변환
    4. 데이터 단위 변환
2. Modeling
    1. colloborative
        1. memory-based
            1. user-based
            2. item-based
        2. model-based
            1. SVD, matrix factorization
            2. ML models
    2. content-based
3. Evaluation
    1. 다양한 평가 방법 사용 후 비교
    2. hybrid 적용
4. Web service
    1. fastapi 로 web 으로 추천시스템 표현해보기


12.7 ~ 12.10 전처리 - 완료 <br>
12.11 ~ 12.15 Modeling <br>
12.16 ~ 12.19 evaluation <br>
12.20 ~ 12.23 웹 구현 <br>

FastAPI 서버 실행
: uvicorn app:app --reload

모델링 방식
1. item-based
2. content-based
3. hybrid

* user-based 를 진행하지 않는 이유
- Cold Start 문제: 사용자가 선택한 레시피 데이터가 한정적이기 때문에 유사한 사용자를 찾기 어렵지 않을까?
- 레시피 중심 추천: 선택한 레시피 자체가 추천의 중심이 되기 때문에 레시피 관련 추천이 더 효과적일 것이라 판단

Item-based
