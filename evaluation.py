import pandas as pd
import numpy as np
from typing import List, Dict, Callable

class RecommenderEvaluator:
    def __init__(self, reviews_df):
        self.reviews_df = reviews_df
    
    def evaluate_recommendations(
        self, 
        recommender_func: Callable[[int], List[Dict]], 
        test_user_ids: List[int], 
        k: int = 5
    ) -> Dict[str, float]:
        precisions = []
        recalls = []
        
        for user_id in test_user_ids:
            # 해당 사용자의 실제 높은 평점 레시피
            user_reviews = self.reviews_df[
                (self.reviews_df['user_id'] == user_id) & 
                (self.reviews_df['rating'] >= 4)
            ]
            
            # 실제 높은 평점 레시피 ID
            actual_high_rated_recipes = set(user_reviews['recipe_id'])
            
            # 추천 시스템으로부터 추천 받은 레시피
            try:
                recommended_recipes = recommender_func(user_id)
                recommended_recipe_ids = set(
                    [rec['recipe_id'] for rec in recommended_recipes]
                )
                
                # 정밀도(Precision) 계산
                if len(recommended_recipe_ids) > 0:
                    precision = len(
                        recommended_recipe_ids.intersection(actual_high_rated_recipes)
                    ) / len(recommended_recipe_ids)
                    precisions.append(precision)
                
                # 재현율(Recall) 계산
                if len(actual_high_rated_recipes) > 0:
                    recall = len(
                        recommended_recipe_ids.intersection(actual_high_rated_recipes)
                    ) / len(actual_high_rated_recipes)
                    recalls.append(recall)
            except Exception as e:
                # 추천을 생성할 수 없는 경우 건너뛰기
                print(f"Error evaluating user {user_id}: {e}")
                continue
        
        # 평균 성능 지표
        return {
            'mean_precision': np.mean(precisions) if precisions else 0,
            'mean_recall': np.mean(recalls) if recalls else 0
        }