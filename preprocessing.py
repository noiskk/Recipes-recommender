import pandas as pd
from recipe_rating import calculate_avg_ratings

# recipes_df
# name, id, minutes, contributor_id, submitted, tags, nutrition, n_steps, steps, description, ingredients, n_ingredients
# 필요 없는 열 : contributor_id, submitted, tags

# reviews_df
# user_id, recipe_id, date, rating, review
# 필요 없는 열 : date, review
# memory-based 할 때는 reviews_df 만 써도 될 듯?
# content-based 할 때는 recipes_df 만 쓰고

def preprocessing():
  # 데이터 불러오기
  recipes_df = pd.read_csv("dataset/RAW_recipes.csv")
  reviews_df = pd.read_csv("dataset/RAW_interactions.csv")

  # 레시피 데이터에서 1/100 추출 (랜덤 샘플링)
  sampled_recipes = recipes_df.sample(frac=0.01, random_state=42)  # 10%만 랜덤으로 추출
  sampled_recipe_ids = set(sampled_recipes['id'])  # 남은 레시피 ID 추출

  # 리뷰 데이터 필터링
  filtered_reviews = reviews_df[reviews_df['recipe_id'].isin(sampled_recipe_ids)]

  # 데이터 전처리
  pp_recipes_df = sampled_recipes.drop(columns= ['contributor_id', 'submitted', 'tags'])
  pp_recipes_df = sampled_recipes.fillna({"name" : "no name", "description" : "no description"})
  pp_reviews_df = filtered_reviews.drop(columns= ['date', 'review'])  
  
  # 평균 평점 계산 및 추가
  recipes_with_ratings = calculate_avg_ratings(pp_recipes_df, pp_reviews_df)

  # 결과를 새로운 CSV 파일로 저장
  recipes_with_ratings.to_csv("dataset/recipes.csv", index=False)
  pp_reviews_df.to_csv("dataset/reviews.csv", index=False)