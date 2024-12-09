import pandas as pd
import numpy as np
import ast
from scipy.sparse import csr_matrix
from content_based import content_based_recommendations
from item_based import item_based_recommendations
from user_based import user_based_recommendations
from recipe_rating import calculate_avg_ratings
from preprocessing import preprocessing

def main():
   # preprocessing()

   recipes_df = pd.read_csv("dataset/recipes.csv")
   reviews_df = pd.read_csv("dataset/reviews.csv")

   # user_item_matrix = pp_reviews_df.pivot_table(index='user_id', columns='recipe_id', values='rating').fillna(0)
   # 위 방식은 용량이 너무 큼. -> sparse matrix 사용  
   sparse_user_item_matrix = csr_matrix((reviews_df['rating'], 
      (reviews_df['user_id'], reviews_df['recipe_id'])))

   # 샘플 유저 100명 선택
   sample_users = reviews_df['user_id'].drop_duplicates().sample(n=100, random_state=42).values 

   # precision과 recall 평가 함수
   def evaluate_recommendations(true_items, recommended_items):
      true_set = set(true_items)
      recommended_set = set(recommended_items)

      # precision과 recall 계산
      precision = len(true_set.intersection(recommended_set)) / len(recommended_set) if recommended_set else 0
      recall = len(true_set.intersection(recommended_set)) / len(true_set) if true_set else 0
      return precision, recall

   # 샘플 유저 100명 선택
   sample_users = reviews_df['user_id'].drop_duplicates().sample(n=100, random_state=42).values
   # 추천 및 평가 결과 저장
   results = []   
   for user_id in sample_users:
       true_items = reviews_df[reviews_df['user_id'] == user_id]['recipe_id'].values   
       # 추천 수행
       recommended_items_user = user_based_recommendations(user_id, sparse_user_item_matrix, top_k=5)
       recommended_items_item = item_based_recommendations(1, sparse_user_item_matrix, top_k=5)  # 예시로 recipe_id 1
       recommended_items_content = content_based_recommendations(user_id, recipes_df, reviews_df, top_k=5)  
       # 평가
       precision_user, recall_user = evaluate_recommendations(true_items, recommended_items_user)
       precision_item, recall_item = evaluate_recommendations(true_items, recommended_items_item)
       precision_content, recall_content = evaluate_recommendations(true_items, recommended_items_content)  
       # 결과 저장
       results.append({
           'user_id': user_id,
           'precision_user': precision_user,
           'recall_user': recall_user,
           'precision_item': precision_item,
           'recall_item': recall_item,
           'precision_content': precision_content,
           'recall_content': recall_content
       })   
   # 결과를 데이터프레임으로 변환
   results_df = pd.DataFrame(results)  
   # 평균 precision과 recall 계산
   average_results = results_df.mean()
   print("평균 Precision 및 Recall:")
   print(average_results)  
   
if __name__ == "__main__":
   main()