import pandas as pd
from sqlalchemy.orm import Session
from database import engine, Recipe, Rating, Base, User
from sqlalchemy.dialects.mysql import insert

def migrate_data():
    # CSV 파일에서 데이터 로드
    recipes_df = pd.read_csv('dataset/recipes.csv')
    ratings_df = pd.read_csv('dataset/reviews.csv')
    
    # 데이터베이스 세션 생성
    session = Session(engine)
    
    try:
        # 레시피 데이터 마이그레이션
        for index, row in recipes_df.iterrows():
            if index % 1000 == 0:  # 진행 상황 표시
                print(f"Processing recipe {index}/{len(recipes_df)}")
                
            recipe = Recipe(
                recipe_id=row['recipe_id'],
                name=row['name'][:255],  # MySQL String 길이 제한
                description=row['description'],
                ingredients=row['ingredients'],
                cooking_time=row.get('cooking_time', 30),  # 기본값 30분
                difficulty=row.get('difficulty', 'medium'),
                category=row.get('category', 'other')
            )
            
            # 중복 처리를 위한 UPSERT
            stmt = insert(Recipe).values(
                recipe_id=recipe.recipe_id,
                name=recipe.name,
                description=recipe.description,
                ingredients=recipe.ingredients,
                cooking_time=recipe.cooking_time,
                difficulty=recipe.difficulty,
                category=recipe.category
            )
            stmt = stmt.on_duplicate_key_update(
                name=recipe.name,
                description=recipe.description,
                ingredients=recipe.ingredients,
                cooking_time=recipe.cooking_time,
                difficulty=recipe.difficulty,
                category=recipe.category
            )
            session.execute(stmt)
            
        # 일괄 커밋
        session.commit()
        print("레시피 데이터 마이그레이션 완료")
        
        # 사용자 데이터 생성 (예시)
        unique_users = ratings_df['user_id'].unique()
        for user_id in unique_users:
            user = User(
                user_id=user_id,
                username=f"user_{user_id}",
                email=f"user_{user_id}@example.com"
            )
            session.add(user)
        
        # 평점 데이터 마이그레이션
        for index, row in ratings_df.iterrows():
            if index % 1000 == 0:  # 진행 상황 표시
                print(f"Processing rating {index}/{len(ratings_df)}")
                
            rating = Rating(
                user_id=row['user_id'],
                recipe_id=row['recipe_id'],
                rating=row['rating'],
                comment=row.get('comment', None)
            )
            session.add(rating)
            
            if index % 1000 == 0:  # 주기적으로 커밋
                session.commit()
        
        # 최종 커밋
        session.commit()
        print("평점 데이터 마이그레이션 완료")
        
    except Exception as e:
        print(f"Error during migration: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    # 데이터베이스 테이블 생성
    Base.metadata.create_all(engine)
    # 데이터 마이그레이션 실행
    migrate_data() 