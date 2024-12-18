import numpy as np
from typing import List
from item_based import ItemBasedRecommender
from content_based import ContentBasedRecommender

class HybridRecommender:
    def __init__(self, reviews_df, recipes_df):
        self.recipes_df = recipes_df
        self.item_based = ItemBasedRecommender(reviews_df, recipes_df)
        self.content_based = ContentBasedRecommender(recipes_df)
    
    def recommend_recipes(self, recipe_ids: List[int], n_recommendations=10):
        """컨텐츠 기반으로 후보를 추출하고 아이템 기반으로 재순위화하는 하이브리드 추천"""
        # 1단계: 컨텐츠 기반으로 더 많은 후보 추출
        content_candidates = self.content_based.recommend_recipes(
            recipe_ids, 
            n_recommendations * 3  # 최종 추천 개수의 3배 (30개)
        )
        
        recipe_scores = {}
        
        # 2단계: 후보들에 대해 아이템 기반 유사도 계산
        for candidate in content_candidates:
            recipe_id = candidate['recipe_id']
            
            # 아이템 기반 유사도 계산
            item_similarities = []
            for selected_id in recipe_ids:
                item_sim = self.item_based.get_similarity(recipe_id, selected_id)
                item_similarities.append(item_sim)
            
            # 아이템 기반 최종 점수 (평균 유사도)
            item_score = np.mean(item_similarities) if item_similarities else 0
            
            recipe_scores[recipe_id] = {
                'recipe_name': candidate['recipe_name'],
                'item_score': item_score,
                'content_score': candidate['similarity_score'],
                'similarities': candidate['similarities'],
                'steps': candidate.get('steps', ''),
                'tags': candidate.get('tags', [])
            }
        
        # 3단계: 아이템 기반 점수로 정렬하여 상위 n개 추천
        sorted_recipes = sorted(
            recipe_scores.items(),
            key=lambda x: x[1]['item_score'],
            reverse=True
        )[:n_recommendations]
        
        return [
            {
                'recipe_id': recipe_id,
                'recipe_name': info['recipe_name'],
                'hybrid_score': sum(s['similarity'] for s in info['similarities']),  # 유사도 합계
                'similarities': info['similarities'],
                'steps': info['steps'],
                'tags': info['tags']
            }
            for recipe_id, info in sorted_recipes
        ] 