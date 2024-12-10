from sklearn.metrics.pairwise import cosine_similarity

def item_based_recommendations(recipe_id, matrix, top_k=5):
    item_similarity = cosine_similarity(matrix.T)  # 아이템 간 코사인 유사도 계산
    similar_items = item_similarity[recipe_id]  # 주어진 아이템과 다른 아이템의 유사도

    # 유사도를 기준으로 정렬
    similar_items[recipe_id] = 0  # 자기 자신 제외
    similar_items_id = similar_items.argsort()[::-1]  # 높은 유사도 순으로 정렬

    # 비슷한 아이템 기반 추천
    recommended_items = similar_items_id[:top_k]
    return recommended_items
