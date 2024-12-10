import pandas as pd

def prepare_recipe_ratings(recipes_df, reviews_df):
    # reviews_df와 recipes_df 병합
    merged_df = pd.merge(reviews_df, recipes_df, left_on='recipe_id', right_on='id')

    # 레시피별 평균 평점 계산
    recipe_ratings = merged_df.groupby('recipe_id')['rating'].mean().reset_index()
    recipe_ratings.columns = ['recipe_id', 'average_rating']

    # 레시피 정보와 평균 평점 병합
    recipes_with_ratings = pd.merge(recipes_df, recipe_ratings, left_on='id', right_on='recipe_id', how='left')
    return recipes_with_ratings

def content_based_recommendations(user_id, recipes_df, pp_reviews_df, top_k=5):
    # 레시피 평점 준비
    recipes_with_ratings = prepare_recipe_ratings(recipes_df, pp_reviews_df)

    user_ratings = pp_reviews_df[pp_reviews_df['user_id'] == user_id]
    user_recipes = recipes_with_ratings[recipes_with_ratings['id'].isin(user_ratings['recipe_id'])]

    # 평점에 영향을 주는 요소를 선택 (예: ingredients, n_steps, minutes 등)
    features = user_recipes[['average_rating', 'n_ingredients', 'minutes']]  # 예시로 선택한 요소들

    # 유사도 계산을 위한 피처 스케일링
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    # 코사인 유사도 계산
    from sklearn.metrics.pairwise import cosine_similarity
    similarity_matrix = cosine_similarity(scaled_features)

    # 추천할 아이템 선택
    recommended_indices = similarity_matrix.argsort()[:, -top_k-1:-1][:, ::-1]  # 상위 K개 추천
    recommended_items = user_recipes.iloc[recommended_indices.flatten()]['id'].values

    return recommended_items
