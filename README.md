# Recipes-recommender

[Dataset](https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions/data?select=RAW_interactions.csv)

가상환경활성화
:source venv/bin/activate

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

Content-based

Hybrid-based

![localhost_3000_](https://github.com/user-attachments/assets/91fd7c7b-1284-4c40-a0b2-dc14deff7be2)
