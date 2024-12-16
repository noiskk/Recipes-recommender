from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

# 가상의 데이터프레임과 추천 시스템 클래스
# 실제로는 pandas 데이터프레임과 추천 시스템 클래스를 사용해야 합니다.
class UserBasedRecommender:
    def recommend_recipes(self, user_id: int, n_recommendations: int = 5) -> List[Dict]:
        # 가상의 추천 결과
        return [{"recipe_id": 1, "recipe_name": "Recipe A", "recommendation_score": 4.5}]

class ItemBasedRecommender:
    def recommend_recipes(self, recipe_id: int, n_recommendations: int = 5) -> List[Dict]:
        # 가상의 추천 결과
        return [{"recipe_id": 2, "recipe_name": "Recipe B", "similarity_score": 4.7}]

# FastAPI 인스턴스 생성
app = FastAPI()

# 추천 시스템 인스턴스 생성
user_based_recommender = UserBasedRecommender()
item_based_recommender = ItemBasedRecommender()

# 사용자 기반 추천 API
@app.get("/recommend/user/{user_id}")
async def recommend_for_user(user_id: int, n_recommendations: int = 5):
    try:
        recommendations = user_based_recommender.recommend_recipes(user_id, n_recommendations)
        if not recommendations:
            raise HTTPException(status_code=404, detail="No recommendations found for this user.")
        return {"user_id": user_id, "recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 아이템 기반 추천 API
@app.get("/recommend/item/{recipe_id}")
async def recommend_for_item(recipe_id: int, n_recommendations: int = 5):
    try:
        recommendations = item_based_recommender.recommend_recipes(recipe_id, n_recommendations)
        if not recommendations:
            raise HTTPException(status_code=404, detail="No recommendations found for this recipe.")
        return {"recipe_id": recipe_id, "recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# uvicorn app:app --reload

# http://127.0.0.1:8000/recommend/user/{user_id}