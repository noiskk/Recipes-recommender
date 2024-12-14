import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class ItemBasedRecommender:
    def __init__(self, reviews_df, recipes_df):
        # 데이터 로드
        self.reviews_df = reviews_df
        self.recipes_df = recipes_df
        
        # 레시피-사용자 평점 행렬 생성
        self.recipe_user_matrix = self._create_recipe_user_matrix()
        
        # 레시피 간 유사도 계산
        self.recipe_similarity_matrix = self._compute_recipe_similarity()

        print(self.recipe_similarity_matrix)
    
    def _create_recipe_user_matrix(self):
        # 레시피-사용자 평점 행렬 생성
        recipe_user_matrix = self.reviews_df.pivot(
            index='recipe_id', 
            columns='user_id', 
            values='rating'
        ).fillna(0)
        return recipe_user_matrix
    
    def _compute_recipe_similarity(self):
        # 레시피 간 코사인 유사도 계산
        recipe_similarity = cosine_similarity(self.recipe_user_matrix.values)
        return pd.DataFrame(
            recipe_similarity, 
            index=self.recipe_user_matrix.index, 
            columns=self.recipe_user_matrix.index
        )
    
    def recommend_recipes(self, user_id, n_recommendations=5):
        # 사용자가 이미 평가한 레시피 찾기
        user_rated_recipes = self.reviews_df[self.reviews_df['user_id'] == user_id]['recipe_id'].unique()
        print(user_rated_recipes)

        # 유사한 레시피 추천
        recommendations = {}
        for recipe_id in user_rated_recipes:
            if recipe_id in self.recipe_similarity_matrix.index:
                similar_recipes = self.recipe_similarity_matrix.loc[recipe_id]
                
                # 유사도 점수 계산
                for similar_recipe_id, similarity_score in similar_recipes.items():
                    if similar_recipe_id not in user_rated_recipes:
                        if similar_recipe_id not in recommendations:
                            recommendations[similar_recipe_id] = 0
                        recommendations[similar_recipe_id] += similarity_score
        
        # 유사도 기준으로 상위 n개 레시피 추천
        top_recommendations = sorted(
            recommendations.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:n_recommendations]
        
        # 추천 레시피 상세 정보 추가
        recommended_recipes = []
        for recipe_id, score in top_recommendations:
            recipe_info = self.recipes_df[self.recipes_df['recipe_id'] == recipe_id]
            if not recipe_info.empty:
                recommended_recipes.append({
                    'recipe_id': recipe_id,
                    'recipe_name': recipe_info['name'].values[0],
                    'similarity_score': score
                })
        
        return recommended_recipes