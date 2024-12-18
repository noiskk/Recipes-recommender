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
    
    def get_similarity(self, recipe_id1, recipe_id2):
        """두 레시피 간의 유사도 반환"""
        if recipe_id1 in self.recipe_similarity_matrix.index and \
           recipe_id2 in self.recipe_similarity_matrix.index:
            return float(self.recipe_similarity_matrix.loc[recipe_id1, recipe_id2])
        return 0.0
    
    def recommend_recipes(self, recipe_ids, n_recommendations=5):
        """선택한 레시피들을 기반으로 추천"""
        recommendations = {}
        selected_recipes = []
        
        # 선택된 레시피 정보 저장
        for recipe_id in recipe_ids:
            recipe_info = self.recipes_df[self.recipes_df['recipe_id'] == recipe_id]
            if not recipe_info.empty:
                selected_recipes.append({
                    'recipe_id': recipe_id,
                    'recipe_name': recipe_info['name'].values[0]
                })
        
        # 유사한 레시피 찾기
        for recipe_id in recipe_ids:
            if recipe_id in self.recipe_similarity_matrix.index:
                similar_recipes = self.recipe_similarity_matrix.loc[recipe_id]
                for similar_recipe_id, similarity_score in similar_recipes.items():
                    if similar_recipe_id not in recipe_ids:
                        if similar_recipe_id not in recommendations:
                            recommendations[similar_recipe_id] = {
                                'score': 0,
                                'similarities': {},
                            }
                        recommendations[similar_recipe_id]['score'] += similarity_score
                        
                        # 각 선택된 레시피와의 유사도 저장
                        sim = self.get_similarity(similar_recipe_id, recipe_id)
                        recipe_name = next(r['recipe_name'] for r in selected_recipes if r['recipe_id'] == recipe_id)
                        recommendations[similar_recipe_id]['similarities'][recipe_id] = {
                            'with_recipe': recipe_name,
                            'similarity': sim
                        }
        
        # 상위 n개 추천
        top_recommendations = sorted(
            recommendations.items(), 
            key=lambda x: x[1]['score'], 
            reverse=True
        )[:n_recommendations]
        
        result = []
        for recipe_id, info in top_recommendations:
            recipe_info = self.recipes_df[self.recipes_df['recipe_id'] == recipe_id]
            if not recipe_info.empty:
                result.append({
                    'recipe_id': recipe_id,
                    'recipe_name': recipe_info['name'].values[0],
                    'similarity_score': float(info['score']),
                    'similarities': list(info['similarities'].values()),  # 딕셔너리 값들을 리스트로 변환
                })
        
        return result