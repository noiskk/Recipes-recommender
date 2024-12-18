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
        # 레시피 내용 결합 (이름, 재료, 조리 방법, 태그)
        self.recipes_df['content'] = (
            self.recipes_df['name'] + ' ' + 
            self.recipes_df['ingredients'].fillna('') + ' ' + 
            self.recipes_df['steps'].fillna('') + ' ' + 
            self.recipes_df['tags'].fillna('').apply(lambda x: ' '.join(eval(x)) if x else '')
        )
        
        # TF-IDF 벡터화
        content_matrix = self.tfidf_vectorizer.fit_transform(
            self.recipes_df['content']
        )
        
        return content_matrix
    
    def get_similarity(self, recipe_id1, recipe_id2):
        """두 레시시피 간의 유사도 반환"""
        idx1 = self.recipes_df[self.recipes_df['recipe_id'] == recipe_id1].index
        idx2 = self.recipes_df[self.recipes_df['recipe_id'] == recipe_id2].index
        
        if len(idx1) > 0 and len(idx2) > 0:
            similarity = cosine_similarity(
                self.content_matrix[idx1[0]:idx1[0]+1], 
                self.content_matrix[idx2[0]:idx2[0]+1]
            )[0][0]
            return float(similarity)
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
        
        # 각 선택된 레시피에 대해 유사한 레시피 찾기
        for recipe_id in recipe_ids:
            recipe_idx = self.recipes_df[
                self.recipes_df['recipe_id'] == recipe_id
            ].index
            
            if len(recipe_idx) > 0:
                similarity_scores = cosine_similarity(
                    self.content_matrix[recipe_idx[0]:recipe_idx[0]+1], 
                    self.content_matrix
                ).flatten()
                
                for idx, score in enumerate(similarity_scores):
                    current_recipe_id = int(self.recipes_df.iloc[idx]['recipe_id'])
                    if current_recipe_id not in recipe_ids:
                        if current_recipe_id not in recommendations:
                            recommendations[current_recipe_id] = {
                                'score': 0,
                                'similarities': {},
                                'steps': self.recipes_df.iloc[idx]['steps'],
                                'tags': eval(self.recipes_df.iloc[idx]['tags']) if not pd.isna(self.recipes_df.iloc[idx]['tags']) else []
                            }
                        recommendations[current_recipe_id]['score'] += score
                        
                        # 각 선택된 레시피와의 유사도 저장
                        sim = self.get_similarity(current_recipe_id, recipe_id)
                        recipe_name = next(r['recipe_name'] for r in selected_recipes if r['recipe_id'] == recipe_id)
                        recommendations[current_recipe_id]['similarities'][recipe_id] = {
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
                    'similarities': list(info['similarities'].values()),
                    'steps': info['steps'],
                    'tags': info['tags']
                })
        
        return result