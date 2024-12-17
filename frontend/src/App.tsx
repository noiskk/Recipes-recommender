import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface Recipe {
  recipe_id: number;
  name: string;
  description: string;
  ingredients: string;
}

function App() {
  const [recipes, setRecipes] = useState<Recipe[]>([]);

  useEffect(() => {
    const fetchRecipes = async () => {
      try {
        const response = await axios.get('http://localhost:8000/recipes');
        setRecipes(response.data.recipes);
      } catch (error) {
        console.error('Error fetching recipes:', error);
      }
    };

    fetchRecipes();
  }, []);

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">레시피 추천 시스템</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {recipes.map(recipe => (
          <div key={recipe.recipe_id} className="p-4 border rounded">
            <h2 className="font-bold">{recipe.name}</h2>
            <p className="text-sm">{recipe.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
