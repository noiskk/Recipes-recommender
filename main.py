import pandas as pd
import numpy as np
import ast
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix

# recipes_df
# name, id, minutes, contributor_id, submitted, tags, nutrition, n_steps, steps, description, ingredients, n_ingredients
# 필요 없는 열 : contributor_id, submitted, tags
# reviews_df
# user_id, recipe_id, date, rating, review
# 필요 없는 열 : date, review
# memory-based 할 때는 reviews_df 만 써도 될 듯?
# content-based 할 때는 recipes_df 만 쓰고

def main():

  pd.set_option('display.max_columns', None)  # 모든 열 출력

  # Loading the data
  recipes_df = pd.read_csv("dataset/RAW_recipes.csv")
  reviews_df = pd.read_csv("dataset/RAW_interactions.csv")

  # preprocessing
  pp_recipes_df = recipes_df.drop(columns= ['contributor_id', 'submitted', 'tags'])
  pp_recipes_df = pp_recipes_df.fillna({"name" : "no name", "description" : "no description"})
  pp_reviews_df = reviews_df.drop(columns= ['date', 'review'])

  # user_item_matrix = pp_reviews_df.pivot_table(index='user_id', columns='recipe_id', values='rating').fillna(0)
  # 위 방식은 용량이 너무 큼. -> sparse matrix 사용

  sparse_user_item_matrix = csr_matrix((pp_reviews_df['rating'], 
     (pp_reviews_df['user_id'], pp_reviews_df['recipe_id'])))
  
  # user-based
  def user_based_recommendations(user_id, matrix, top_k=5):
     # 사용자 간 코사인 유사도 계산
     user_similarity = cosine_similarity(matrix)
     similar_users = user_similarity[user_id]  # 주어진 사용자와 다른 사용자의 유사도

     # 유사도를 기준으로 정렬
     similar_users[user_id] = 0 # 자기 자신 제외
     similar_users_id = similar_users.argsort()[::-1] # 높은 유사도 순으로 정렬

     # 비슷한 사용자가 평가한 아이템 기반 추천
     scores = matrix[similar_users_id].toarray().sum(axis=0) # 비슷한 사용자들의 평가 합산
     
     recommended_items = scores.argsort()[::-1][:top_k]
     return recommended_items

  recommended_items = user_based_recommendations(0, sparse_user_item_matrix, top_k=5)
  print("user-based : ", recommended_items)




if __name__ == "__main__":
    main()