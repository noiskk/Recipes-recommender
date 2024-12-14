import pandas as pd
from user_based import UserBasedRecommender
from item_based import ItemBasedRecommender
from content_based import ContentBasedRecommender
from evaluation import RecommenderEvaluator

class RecipeRecommendationSystem:
    def __init__(self, reviews_path, recipes_path):
        # 중앙 집중식 데이터 로드
        self.reviews_df = pd.read_csv(reviews_path)
        self.recipes_df = pd.read_csv(recipes_path)
        
        # 각 추천 시스템 초기화
        self.user_based_recommender = UserBasedRecommender(
            self.reviews_df, self.recipes_df
        )
        self.item_based_recommender = ItemBasedRecommender(
            self.reviews_df, self.recipes_df
        )
        self.content_based_recommender = ContentBasedRecommender(
            self.recipes_df
        )
        
        # 평가기 초기화
        self.evaluator = RecommenderEvaluator(self.reviews_df)
    
    def recommend_user_based(self, user_id, n_recommendations=5):
        return self.user_based_recommender.recommend_recipes(user_id, n_recommendations)
    
    def recommend_item_based(self, user_id, n_recommendations=5):
        return self.item_based_recommender.recommend_recipes(user_id, n_recommendations)
    
    def recommend_content_based(self, recipe_id, n_recommendations=5):
        return self.content_based_recommender.recommend_recipes(recipe_id, n_recommendations)
    
    def evaluate_recommenders(self, test_user_ids=None, k=5):
        if test_user_ids is None:
            # 기본적으로 일부 사용자 샘플링
            test_user_ids = self.reviews_df['user_id'].sample(n=100).tolist()
        
        evaluation_results = {
            'User-Based': self.evaluator.evaluate_recommendations(
                lambda user_id: self.recommend_user_based(user_id), 
                test_user_ids, k
            ),
            'Item-Based': self.evaluator.evaluate_recommendations(
                lambda user_id: self.item_based_recommender.recommend_recipes(
                    self.reviews_df[
                        self.reviews_df['user_id'] == user_id
                    ]['recipe_id'].iloc[0] if not self.reviews_df[self.reviews_df['user_id'] == user_id].empty else None
                ), 
                test_user_ids, k
            ),
            'Content-Based': self.evaluator.evaluate_recommendations(
                lambda user_id: self.content_based_recommender.recommend_recipes(
                    self.reviews_df[
                        self.reviews_df['user_id'] == user_id
                    ]['recipe_id'].iloc[0] if not self.reviews_df[self.reviews_df['user_id'] == user_id].empty else None
                ), 
                test_user_ids, k
            )
        }
        
        return evaluation_results

def main():
    # 데이터 경로 설정
    REVIEWS_PATH = 'dataset/reviews.csv'
    RECIPES_PATH = 'dataset/recipes.csv'
    
    # 추천 시스템 인스턴스 생성
    recomm_system = RecipeRecommendationSystem(REVIEWS_PATH, RECIPES_PATH)
    
    # 예시 사용자 및 레시피 ID
    example_user_id = 88378
    example_recipe_id = 310201
    
    # 각 추천 방식 데모
    print("User-Based 추천:")
    user_based_recs = recomm_system.recommend_user_based(example_user_id)
    for rec in user_based_recs:
        print(f"- {rec['recipe_id']} (Score: {rec.get('recommendation_score', rec.get('similarity_score'))})")
     
    print("\nItem-Based 추천:")
    item_based_recs = recomm_system.recommend_item_based(example_user_id)
    for rec in item_based_recs:
        print(f"- {rec['recipe_id']} (Score: {rec.get('recommendation_score', rec.get('similarity_score'))})")
    
    print("\nContent-Based 추천:")
    content_based_recs = recomm_system.recommend_content_based(example_recipe_id)
    for rec in content_based_recs:
        print(f"- {rec['recipe_id']} (Score: {rec.get('recommendation_score', rec.get('similarity_score'))})")
    
    # 추천 시스템 평가
   #  print("\n추천 시스템 평가 결과:")
   #  evaluation_results = recomm_system.evaluate_recommenders()
   #  for name, results in evaluation_results.items():
   #      print(f"{name} 추천 시스템:")
   #      print(f"  평균 정밀도(Precision): {results['mean_precision']:.4f}")
   #      print(f"  평균 재현율(Recall): {results['mean_recall']:.4f}")

if __name__ == "__main__":
    main()