import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface Recipe {
  recipe_id: number;
  name: string;
  description: string;
  ingredients: string;
}

interface Similarity {
  with_recipe: string;
  similarity: number;
}

interface Recommendation {
  recipe_id: number;
  recipe_name: string;
  similarity_score?: number;
  hybrid_score?: number;
  similarities: Similarity[];
}

function App() {
  const [recipes, setRecipes] = useState<Recipe[]>([]);
  const [selectedRecipes, setSelectedRecipes] = useState<number[]>([]);
  const [recommendations, setRecommendations] = useState<{
    user_based: Recommendation[];
    item_based: Recommendation[];
    content_based: Recommendation[];
    hybrid: Recommendation[];
  } | null>(null);

  useEffect(() => {
    fetchRecipes();
  }, []);

  const fetchRecipes = async () => {
    try {
      const response = await axios.get('http://localhost:8000/recipes');
      setRecipes(response.data.recipes);
    } catch (error) {
      console.error('Error fetching recipes:', error);
    }
  };

  const handleRecipeSelect = (recipeId: number) => {
    setSelectedRecipes(prev => 
      prev.includes(recipeId) 
        ? prev.filter(id => id !== recipeId)
        : [...prev, recipeId]
    );
  };

  const getRecommendations = async () => {
    try {
      const response = await axios.post('http://localhost:8000/recommend', {
        recipe_ids: selectedRecipes
      });
      setRecommendations(response.data);
    } catch (error) {
      console.error('Error getting recommendations:', error);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">레시피 추천 시스템</h1>
      
      {/* 레시피 목록 */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-4">
        {recipes.map(recipe => (
          <div 
            key={recipe.recipe_id}
            className={`p-4 border rounded cursor-pointer ${
              selectedRecipes.includes(recipe.recipe_id) ? 'bg-blue-100' : ''
            }`}
            onClick={() => handleRecipeSelect(recipe.recipe_id)}
          >
            <h2 className="font-bold">{recipe.name}</h2>
            <p className="text-sm">{recipe.description}</p>
          </div>
        ))}
      </div>

      {/* 추천 받기 버튼 */}
      <button
        onClick={getRecommendations}
        className="w-full py-2 bg-blue-500 text-white rounded mb-4"
        disabled={selectedRecipes.length === 0}
      >
        추천 받기
      </button>

      {/* 추천 결과 */}
      {recommendations && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <h3 className="font-bold mb-2">하이브리드 추천</h3>
            {recommendations.hybrid.map(rec => (
              <div key={rec.recipe_id} className="p-2 border rounded mb-2">
                <p className="font-medium">{rec.recipe_name}</p>
                <p className="text-sm text-gray-600">
                  종합 점수: {rec.hybrid_score?.toFixed(2)}
                </p>
                <div className="mt-2">
                  <p className="text-xs font-medium">선택한 레시피와의 유사도:</p>
                  {rec.similarities.map((sim, idx) => (
                    <p key={idx} className="text-xs text-gray-500">
                      {sim.with_recipe}: {sim.similarity.toFixed(2)}
                    </p>
                  ))}
                </div>
              </div>
            ))}
          </div>

          <div>
            <h3 className="font-bold mb-2">아이템 기반 추천</h3>
            {recommendations.item_based.map(rec => (
              <div key={rec.recipe_id} className="p-2 border rounded mb-2">
                <p className="font-medium">{rec.recipe_name}</p>
                <p className="text-sm text-gray-600">
                  종합 점수: {rec.similarity_score?.toFixed(2)}
                </p>
                <div className="mt-2">
                  <p className="text-xs font-medium">선택한 레시피와의 유사도:</p>
                  {rec.similarities.map((sim, idx) => (
                    <p key={idx} className="text-xs text-gray-500">
                      {sim.with_recipe}: {sim.similarity.toFixed(2)}
                    </p>
                  ))}
                </div>
              </div>
            ))}
          </div>

          <div>
            <h3 className="font-bold mb-2">컨텐츠 기반 추천</h3>
            {recommendations.content_based.map(rec => (
              <div key={rec.recipe_id} className="p-2 border rounded mb-2">
                <p className="font-medium">{rec.recipe_name}</p>
                <p className="text-sm text-gray-600">
                  종합 점수: {rec.similarity_score?.toFixed(2)}
                </p>
                <div className="mt-2">
                  <p className="text-xs font-medium">선택한 레시피와의 유사도:</p>
                  {rec.similarities.map((sim, idx) => (
                    <p key={idx} className="text-xs text-gray-500">
                      {sim.with_recipe}: {sim.similarity.toFixed(2)}
                    </p>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
