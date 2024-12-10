import pandas as pd

def calculate_avg_ratings(recipes_df, reviews_df):
      # reviews_df 에서 레시피별 평균 평점 계산
      recipe_ratings = reviews_df.groupby("recipe_id")["rating"].mean().reset_index()
      recipe_ratings.columns = ["recipe_id", "average_rating"]

      # recipes_df 와 평균 평점 병합
      recipes_with_ratings = pd.merge(recipes_df, recipe_ratings, left_on="id", right_on="recipe_id", how="left")

      # 평점이 없는 레시피 드롭
      recipes_with_ratings = recipes_with_ratings.dropna(subset=["average_rating"])

      return recipes_with_ratings