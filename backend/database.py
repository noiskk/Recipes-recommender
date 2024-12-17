from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime

load_dotenv()

DATABASE_URL = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"

engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=3600
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 데이터베이스 모델
class Recipe(Base):
    __tablename__ = "recipes"
    
    recipe_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(Text)
    ingredients = Column(Text)
    cooking_time = Column(Integer)  # 조리 시간(분)
    difficulty = Column(String(20))  # 난이도
    category = Column(String(50))    # 카테고리
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    ratings = relationship("Rating", back_populates="recipe")
    
class User(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    ratings = relationship("Rating", back_populates="user")
    
class Rating(Base):
    __tablename__ = "ratings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    recipe_id = Column(Integer, ForeignKey("recipes.recipe_id"))
    rating = Column(Float)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    user = relationship("User", back_populates="ratings")
    recipe = relationship("Recipe", back_populates="ratings")

class UserPreference(Base):
    __tablename__ = "user_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    category = Column(String(50))    # 선호 카테고리
    ingredient = Column(String(100)) # 선호/기피 재료
    preference_type = Column(String(20))  # 'like' or 'dislike'

# 데이터베이스 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 