-- 레시피 검색 최적화
CREATE INDEX idx_recipe_name ON recipes(name);
CREATE INDEX idx_recipe_category ON recipes(category);

-- 평점 조회 최적화
CREATE INDEX idx_rating_user ON ratings(user_id);
CREATE INDEX idx_rating_recipe ON ratings(recipe_id);
CREATE INDEX idx_rating_created ON ratings(created_at);

-- 사용자 선호도 검색 최적화
CREATE INDEX idx_preference_user ON user_preferences(user_id);
CREATE INDEX idx_preference_category ON user_preferences(category); 