from sklearn.metrics.pairwise import cosine_similarity

def user_based_recommendations(user_id, matrix, top_k=5):
    # 사용자 간 코사인 유사도 계산
    user_similarity = cosine_similarity(matrix)
    similar_users = user_similarity[user_id]  # 주어진 사용자와 다른 사용자의 유사도

    # 유사도를 기준으로 정렬
    similar_users[user_id] = 0  # 자기 자신 제외
    similar_users_id = similar_users.argsort()[::-1]  # 높은 유사도 순으로 정렬

    # 비슷한 사용자가 평가한 아이템 기반 추천
    scores = matrix[similar_users_id].toarray().sum(axis=0)  # 비슷한 사용자들의 평가 합산
    
    recommended_items = scores.argsort()[::-1][:top_k]
    return recommended_items
