import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ContentBasedRecommender:
    def __init__(self, recipes_df):
        # 데이터 로드
        self.recipes_df = recipes_df
        
        # 콘텐츠 벡터화
        self.tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        self.content_matrix = self._create_content_matrix()
    
    def _create_content_matrix(self):
        # 레시피 내용 결합 (예: 이름, 재료, 요리 설명 등)
        self.recipes_df['content'] = self.recipes_df['name'] + ' ' + \
                                     self.recipes_df['ingredients'].fillna('') + ' ' + \
                                     self.recipes_df['steps'].fillna('')
        
        # TF-IDF 벡터화
        content_matrix = self.tfidf_vectorizer.fit_transform(
            self.recipes_df['content']
        )
        return content_matrix
    
    def recommend_recipes(self, recipe_id, n_recommendations=5):
        # 주어진 레시피의 인덱스 찾기
        recipe_indices = self.recipes_df[
            self.recipes_df['recipe_id'] == recipe_id
        ].index

        # 레시피를 찾지 못한 경우 빈 리스트 반환
        if len(recipe_indices) == 0:
            return []
        
        recipe_index = recipe_indices[0]
        
        # 코사인 유사도 계산
        similarity_scores = cosine_similarity(
            self.content_matrix[recipe_index], 
            self.content_matrix
        ).flatten()
        
        # 가장 유사한 레시피 찾기 (자기 자신 제외)
        similar_indices = similarity_scores.argsort()[::-1][1:n_recommendations+1]
        
        # 추천 레시피 상세 정보 추가
        recommended_recipes = []
        for idx in similar_indices:
            recommended_recipes.append({
                'recipe_id': self.recipes_df.loc[idx, 'recipe_id'],
                'recipe_name': self.recipes_df.loc[idx, 'name'],
                'similarity_score': similarity_scores[idx]
            })
        
        return recommended_recipes
    
    def recommend_recipes_from_history(self, recipe_ids, n_recommendations=5):
        """선택한 레시피들을 기반으로 추천"""
        recommendations = {}
        
        # 각 선택된 레시피에 대해 유사한 레시피 찾기
        for recipe_id in recipe_ids:
            recipe_indices = self.recipes_df[
                self.recipes_df['recipe_id'] == recipe_id
            ].index
            
            if len(recipe_indices) > 0:
                recipe_index = recipe_indices[0]
                
                # 코사인 유사도 계산
                similarity_scores = cosine_similarity(
                    self.content_matrix[recipe_index], 
                    self.content_matrix
                ).flatten()
                
                # 각 레시피와의 유사도 저장
                for idx, score in enumerate(similarity_scores):
                    current_recipe_id = int(self.recipes_df.iloc[idx]['recipe_id'])
                    if current_recipe_id not in recipe_ids:  # 이미 선택된 레시피 제외
                        if current_recipe_id not in recommendations:
                            recommendations[current_recipe_id] = 0
                        recommendations[current_recipe_id] += float(score)
        
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
                    'recipe_id': int(recipe_id),
                    'recipe_name': str(recipe_info['name'].values[0]),
                    'similarity_score': float(score)
                })
        
        return recommended_recipes