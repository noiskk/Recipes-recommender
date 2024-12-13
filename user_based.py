from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def user_based_recommendations(user_id, matrix, top_k=5):
    # 사용자 간 코사인 유사도 계산
    user_similarity = cosine_similarity(matrix, dense_output=False)

    # user_id와 인덱스 매핑 생성
    user_ids = matrix.nonzero()[0]  # 희소 행렬의 사용자 인덱스
    user_id_to_index = {user_id: index for index, user_id in enumerate(user_ids)}

    # user_id를 인덱스로 변환
    if user_id in user_id_to_index:
        user_index = user_id_to_index[user_id]
    else:
        raise ValueError(f"User ID {user_id} is not in the user-item matrix.")

    # 유사한 사용자 찾기
    similar_users = user_similarity[user_index].toarray().flatten()  # 주어진 사용자와 다른 사용자의 유사도

    # 유사도를 기준으로 정렬
    similar_users[user_index] = 0  # 자기 자신 제외
    similar_users_id = np.argsort(similar_users)[::-1]  # 높은 유사도 순으로 정렬

    # 비슷한 사용자가 평가한 아이템 기반 추천
    scores = matrix[similar_users_id].sum(axis=0)  # 비슷한 사용자들의 평가 합산
    
    recommended_items = np.argsort(scores)[::-1][:top_k]
    return recommended_items
