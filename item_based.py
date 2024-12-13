from sklearn.metrics.pairwise import cosine_similarity

def item_based_recommendations(recipe_id, matrix, top_k=5):
    # 아이템 간 코사인 유사도 계산
    item_similarity = cosine_similarity(matrix, dense_output=False)  # 희소 행렬로 유사도 계산

    # recipe_id와 인덱스 매핑 생성
    recipe_ids = matrix.nonzero()[1]  # 희소 행렬의 아이템 인덱스
    recipe_id_to_index = {recipe_id: index for index, recipe_id in zip(recipe_ids, range(len(recipe_ids)))}

    # recipe_id를 인덱스로 변환
    if recipe_id in recipe_id_to_index:
        recipe_index = recipe_id_to_index[recipe_id]
    else:
        raise ValueError(f"Recipe ID {recipe_id} is not in the item-item matrix.")

    similar_items = item_similarity[recipe_index]  # 주어진 아이템과 다른 아이템의 유사도

    # 유사도를 기준으로 정렬
    similar_items[recipe_index] = 0  # 자기 자신 제외
    similar_items_id = similar_items.argsort()[::-1]  # 높은 유사도 순으로 정렬

    # 비슷한 아이템 기반 추천
    recommended_items = similar_items_id[:top_k]
    return recommended_items
