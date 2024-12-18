import pandas as pd
from item_based import ItemBasedRecommender
from content_based import ContentBasedRecommender
from hybrid import HybridRecommender
from typing import List

class RecipeRecommendationSystem:
    def __init__(self, reviews_path, recipes_path):
        # 중앙 집중식 데이터 로드
        self.reviews_df = pd.read_csv(reviews_path)
        self.recipes_df = pd.read_csv(recipes_path)
        
        # 각 추천 시스템 초기화
        self.hybrid_recommender = HybridRecommender(
            self.reviews_df, self.recipes_df
        )
        self.item_based_recommender = ItemBasedRecommender(
            self.reviews_df, self.recipes_df
        )
        self.content_based_recommender = ContentBasedRecommender(
            self.recipes_df
        )
    
    def get_recipe_list(self, page: int = 1, limit: int = 20):
        """페이지네이션된 레시피 목록 반환"""
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        
        return self.recipes_df.iloc[start_idx:end_idx][
            ['recipe_id', 'name', 'description', 'ingredients']
        ].to_dict('records')
    
    def recommend_hybrid_from_history(
        self, recipe_ids: List[int], n_recommendations: int = 10
    ):
        """하이브리드 추천"""
        return self.hybrid_recommender.recommend_recipes(
            recipe_ids, n_recommendations
        )
    
    def recommend_item_based_from_history(
        self, recipe_ids: List[int], n_recommendations: int = 10
    ):
        """아이템 기반 협업 필터링"""
        return self.item_based_recommender.recommend_recipes(
            recipe_ids, n_recommendations
        )
    
    def recommend_content_based_from_history(
        self, recipe_ids: List[int], n_recommendations: int = 10
    ):
        """컨텐츠 기반 필터링"""
        return self.content_based_recommender.recommend_recipes(
            recipe_ids, n_recommendations
        )
    
    def _create_temp_user_profile(self, recipe_ids: List[int]):
        """임시 사용자 프로필 생성"""
        return {recipe_id: 5.0 for recipe_id in recipe_ids}