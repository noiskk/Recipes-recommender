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