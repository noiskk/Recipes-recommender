from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from main import RecipeRecommendationSystem
from sqlalchemy.orm import Session
from database import get_db, Recipe, Rating, User, UserPreference

# Pydantic 모델 정의
class RecipeSubmission(BaseModel):
    recipe_ids: List[int]

# 실제 추천 시스템 초기화
recommender = RecipeRecommendationSystem(
    reviews_path='../dataset/reviews.csv',
    recipes_path='../dataset/recipes.csv'
)

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 전체 레시피 목록 조회 API
@app.get("/recipes")
async def get_recipes(
    page: int = 1, 
    limit: int = 20, 
    db: Session = Depends(get_db)
):
    skip = (page - 1) * limit
    recipes = db.query(Recipe).offset(skip).limit(limit).all()
    total = db.query(Recipe).count()
    
    return {
        "recipes": recipes,
        "total": total,
        "page": page,
        "limit": limit
    }

# 사용자 선택 레시피 기반 추천 API
@app.post("/recommend")
async def get_recommendations(submission: RecipeSubmission):
    try:
        print(f"Received recipe_ids: {submission.recipe_ids}")
        
        # 각 추천 방식별 결과
        user_based_recs = recommender.recommend_user_based_from_history(
            submission.recipe_ids
        )
        print(f"User-based recommendations: {user_based_recs}")
        
        item_based_recs = recommender.recommend_item_based_from_history(
            submission.recipe_ids
        )
        print(f"Item-based recommendations: {item_based_recs}")
        
        content_based_recs = recommender.recommend_content_based_from_history(
            submission.recipe_ids
        )
        print(f"Content-based recommendations: {content_based_recs}")
        
        return {
            "user_based": user_based_recs,
            "item_based": item_based_recs,
            "content_based": content_based_recs
        }
    except Exception as e:
        print(f"Error in recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ratings")
async def create_rating(
    user_id: int,
    recipe_id: int,
    rating: float,
    db: Session = Depends(get_db)
):
    db_rating = Rating(
        user_id=user_id,
        recipe_id=recipe_id,
        rating=rating
    )
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating

@app.get("/recipes/search")
async def search_recipes(
    query: str = None,
    category: str = None,
    difficulty: str = None,
    page: int = 1,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    query = db.query(Recipe)
    
    if query:
        query = query.filter(Recipe.name.ilike(f"%{query}%"))
    if category:
        query = query.filter(Recipe.category == category)
    if difficulty:
        query = query.filter(Recipe.difficulty == difficulty)
        
    total = query.count()
    recipes = query.offset((page-1)*limit).limit(limit).all()
    
    return {
        "total": total,
        "page": page,
        "recipes": recipes
    }

@app.get("/users/{user_id}/preferences")
async def get_user_preferences(
    user_id: int,
    db: Session = Depends(get_db)
):
    preferences = db.query(UserPreference).filter(
        UserPreference.user_id == user_id
    ).all()
    return preferences

# uvicorn app:app --reload

# http://127.0.0.1:8000/recipes
# http://127.0.0.1:8000/recommend