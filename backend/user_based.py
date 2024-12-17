import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class UserBasedRecommender:
    def __init__(self, reviews_df, recipes_df):
        # 데이터 로드
        self.reviews_df = reviews_df
        self.recipes_df = recipes_df
        
        # 사용자-레시피 평점 행렬 생성
        self.user_recipe_matrix = self._create_user_recipe_matrix()
        
    def _create_user_recipe_matrix(self):
        # 사용자-레시피 평점 행렬 생성
        user_recipe_matrix = self.reviews_df.pivot(
            index='user_id', 
            columns='recipe_id', 
            values='rating'
        ).fillna(0)

        return user_recipe_matrix
    
    def get_similar_users(self, user_id, n_users=100):
        # 코사인 유사도를 이용한 유사한 사용자 찾기
        user_similarities = cosine_similarity(
            self.user_recipe_matrix.loc[user_id].values.reshape(1, -1), 
            self.user_recipe_matrix.values
        )[0]
        
        # 가장 유사한 사용자들 찾기 (자기 자신 제외)
        similar_users_indices = user_similarities.argsort()[::-1][1:n_users+1]
        similar_users = self.user_recipe_matrix.index[similar_users_indices]
        
        return similar_users
    
    def recommend_recipes(self, user_id, n_recommendations=5):
        similar_users = self.get_similar_users(user_id)

        # 사용자가 아직 평가하지 않은 레시피 찾기
        user_rated_recipes = self.user_recipe_matrix.loc[user_id]
        print(user_rated_recipes)
        unrated_recipes = user_rated_recipes[user_rated_recipes == 0].index

        # 유사 사용자들의 추천 레시피 계산
        recommendations = {}
        for recipe_id in unrated_recipes:
            recipe_ratings = self.user_recipe_matrix.loc[similar_users, recipe_id]
            avg_rating = recipe_ratings[recipe_ratings > 0].mean()
            # if not np.isnan(avg_rating):  # 평균이 nan이 아닌 경우에만 추가
            recommendations[recipe_id] = avg_rating

        # 평점 기준으로 상위 n개 레시피 추천
        top_recommendations = sorted(
            recommendations.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:n_recommendations]

        # 레시피 상세 정보 추가
        recommended_recipes = []
        for recipe_id, score in top_recommendations:
            recipe_info = self.recipes_df[self.recipes_df['recipe_id'] == recipe_id]
            if not recipe_info.empty:
                recommended_recipes.append({
                    'recipe_id': recipe_id,
                    'recipe_name': recipe_info['name'].values[0],
                    'recommendation_score': score
                })

        return recommended_recipes
    
    def recommend_recipes_from_profile(self, user_profile, n_recommendations=5):
        """임시 사용자 프로필을 기반으로 추천"""
        # 임시 사용자 벡터 생성
        temp_user_vector = np.zeros(len(self.user_recipe_matrix.columns))
        for recipe_id, rating in user_profile.items():
            if recipe_id in self.user_recipe_matrix.columns:
                col_idx = self.user_recipe_matrix.columns.get_loc(recipe_id)
                temp_user_vector[col_idx] = rating
        
        # 유사도 계산
        similarities = cosine_similarity([temp_user_vector], self.user_recipe_matrix.values)[0]
        
        # 가장 유사한 사용자들의 평점 가져오기
        similar_users_indices = similarities.argsort()[::-1][:10]  # 상위 10명
        similar_users = self.user_recipe_matrix.index[similar_users_indices]
        
        # 추천 계산
        recommendations = {}
        rated_recipes = list(user_profile.keys())
        
        for recipe_id in self.user_recipe_matrix.columns:
            if recipe_id not in rated_recipes:
                ratings = self.user_recipe_matrix.loc[similar_users, recipe_id]
                avg_rating = ratings[ratings > 0].mean()
                if not np.isnan(avg_rating):
                    recommendations[recipe_id] = avg_rating
        
        # 상위 n개 추천
        top_recommendations = sorted(
            recommendations.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:n_recommendations]
        
        # 추천 결과 포맷팅
        result = []
        for recipe_id, score in top_recommendations:
            recipe_info = self.recipes_df[self.recipes_df['recipe_id'] == recipe_id]
            if not recipe_info.empty:
                result.append({
                    'recipe_id': recipe_id,
                    'recipe_name': recipe_info['name'].values[0],
                    'recommendation_score': score
                })
        
        return result