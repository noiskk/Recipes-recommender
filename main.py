import pandas as pd
import ast

def main():

  pd.set_option('display.max_columns', None)  # 모든 열 출력

  #Loading the data
  recipes_df = pd.read_csv("dataset/RAW_recipes.csv")
  reviews_df = pd.read_csv("dataset/RAW_interactions.csv")

  # recipes_df
  # name, id, minutes, contributor_id, submitted, tags, nutrition, n_steps, steps, description, ingredients, n_ingredients
  # 필요 없는 열 : contributor_id, submitted, tags

  # reviews_df
  # user_id, recipe_id, date, rating, review
  # 필요 없는 열 : date, review

  # memory-based 할 때는 reviews_df 만 써도 될 듯?
  # content-based 할 때는 recipes_df 만 쓰고
  

  print(recipes_df)
  print(recipes_df.isnull().sum())

if __name__ == "__main__":
    main()