import os
import json
from google import genai
from google.genai import types
from pydantic import BaseModel
from dotenv import load_dotenv

_client = None
def get_client():
    global _client
    if _client is None:
        load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
        if "GEMINI_API_KEY" not in os.environ or not os.environ["GEMINI_API_KEY"].strip():
            return None
        try:
            _client = genai.Client()
        except Exception:
            return None
    return _client

class NarratorOutput(BaseModel):
    display_title: str
    ingredients: list[str]
    steps: list[str]
    servings: int
    tags: list[str]
    note: str
    cooking_time: str
    difficulty: str
    description: str

def narrate_recipe(recipe: dict) -> dict:
    """Use Gemini to enrich the recipe title, add emojis, description, cooking time, and a friendly note."""
    client = get_client()
    if client is None:
        # Fallback to rule-based recipe narration if API fails
        title = recipe.get("title", "Delicious Dish")
        tags = recipe.get("tags", [])
        
        title_lower = title.lower()
        if "biryani" in title_lower:
            emoji = "🍛"
            cooking_time = "40–50 mins"
            difficulty = "⭐⭐⭐ Hard"
            description = "A rich, fragrant Biryani cooked with premium basmati rice, tender elements, aromatic spices, and warm ghee."
        elif "pulao" in title_lower:
            emoji = "🍛"
            cooking_time = "25–30 mins"
            difficulty = "⭐⭐ Medium"
            description = "A fragrant, spiced vegetarian rice dish cooked gently in ghee with aromatic herbs."
        elif "fried rice" in title_lower:
            emoji = "🍚"
            cooking_time = "10–15 mins"
            difficulty = "⭐ Easy"
            description = "A classic stir-fried rice tossed with veggies, seasonings, and soy sauce on high heat."
        elif "pasta" in title_lower:
            emoji = "🍝"
            cooking_time = "15–20 mins"
            difficulty = "⭐⭐ Medium"
            description = "A delightful, comforting pasta dish cooked to perfection with flavorful seasoning and fresh ingredients."
        elif "rice" in title_lower:
            emoji = "🍛"
            cooking_time = "20–30 mins"
            difficulty = "⭐⭐ Medium"
            description = "A wholesome, filling rice bowl packed with vibrant veggies and savory elements."
        elif "salad" in title_lower:
            emoji = "🥗"
            cooking_time = "10–15 mins"
            difficulty = "⭐ Easy"
            description = "A crisp, refreshing garden salad tossed in a light olive oil dressing, perfect as a healthy meal or side."
        elif "sandwich" in title_lower:
            emoji = "🥪"
            cooking_time = "5–10 mins"
            difficulty = "⭐ Easy"
            description = "A fresh, crisp sandwich layered with ingredients between perfectly toasted bread."
        elif "omelette" in title_lower:
            emoji = "🍳"
            cooking_time = "5–10 mins"
            difficulty = "⭐ Easy"
            description = "A fluffy, golden omelette folded with flavorful ingredients, perfect for breakfast or a quick snack."
        elif "soup" in title_lower:
            emoji = "🥣"
            cooking_time = "15–20 mins"
            difficulty = "⭐ Easy"
            description = "A warm, soothing homemade soup simmering with rich flavors and tender ingredients."
        elif "stir-fry" in title_lower:
            emoji = "🥢"
            cooking_time = "10–15 mins"
            difficulty = "⭐⭐ Medium"
            description = "A vibrant, sizzling stir-fry tossed in a flavorful sauce and cooked over high heat."
        else:
            emoji = "🍳"
            cooking_time = "20–30 mins"
            difficulty = "⭐ Easy"
            description = "A quick, pan-seared mixture of delicious ingredients seasoned to taste."
            
        display_title = f"Chef's Special {title} {emoji}"
        
        step_emojis = ["🔪", "🔥", "🍽️", "✨", "⭐"]
        original_steps = recipe.get("steps", [])
        narrated_steps = []
        
        for idx, step in enumerate(original_steps):
            prefix = step_emojis[idx] if idx < len(step_emojis) else "⭐"
            # Strip existing emojis if present to avoid doubling
            step_clean = step
            parts = step.split(" ", 1)
            if len(parts) > 1 and len(parts[0]) <= 2:
                step_clean = parts[1]
            narrated_steps.append(f"{prefix} {step_clean}")
            
        note = "Bon appétit! Made with love and your favorite ingredients. Enjoy your homemade creation! ❤️"
        
        return {
            "display_title": display_title,
            "ingredients": recipe.get("ingredients", []),
            "steps": narrated_steps,
            "servings": recipe.get("servings", 2),
            "tags": tags,
            "note": note,
            "cooking_time": cooking_time,
            "difficulty": difficulty,
            "description": description
        }
        
    try:
        prompt = f"""
        You are the Master Chef Narrator Agent for Chef AI. Take the following recipe details:
        Title: {recipe.get('title')}
        Servings: {recipe.get('servings')}
        Ingredients: {', '.join(recipe.get('ingredients', []))}
        Instructions:
        {chr(10).join(f"- {step}" for step in recipe.get('steps', []))}
        Tags: {', '.join(recipe.get('tags', []))}
        
        Perform the following tasks:
        1. Create a fun, cheerful, and engaging display title for the recipe. Prepend "Chef's Special" and append a relevant food emoji (e.g. "Chef's Special Chicken Biryani 🍛" or "Chef's Special Garlic Bread 🍞").
        2. Set a realistic cooking time estimate (e.g., '15–20 mins', '40–50 mins').
        3. Set a difficulty level (e.g., '⭐ Easy', '⭐⭐ Medium', '⭐⭐⭐ Hard').
        4. Write a warm, mouthwatering, engaging description of the dish (1-2 sentences).
        5. For each of the 5 instruction steps, prepend a relevant cooking emoji at the beginning (e.g. 🔪 for chopping, 🔥 or 🍳 for cooking, 🧂 for seasoning, 🍽️ or ✨ for plating/finishing). Ensure you preserve the full instruction text.
        6. Write a friendly, enthusiastic chef note at the end to encourage the cook, concluding with "Bon appétit!" and a heart emoji.
        
        Ensure your output matches the requested JSON schema.
        """
        
        response = client.models.generate_content(
            model='gemini-3.1-flash-lite',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=NarratorOutput,
                temperature=0.7
            )
        )
        
        result = json.loads(response.text)
        return {
            "display_title": result.get("display_title", f"Chef's Special {recipe.get('title')} 🍳"),
            "ingredients": result.get("ingredients", recipe.get("ingredients", [])),
            "steps": result.get("steps", recipe.get("steps", [])),
            "servings": result.get("servings", recipe.get("servings", 2)),
            "tags": result.get("tags", recipe.get("tags", [])),
            "note": result.get("note", "Enjoy your delicious homemade meal! ❤️"),
            "cooking_time": result.get("cooking_time", "20-30 mins"),
            "difficulty": result.get("difficulty", "⭐⭐ Medium"),
            "description": result.get("description", "A tasty homemade creation prepared with fresh ingredients.")
        }
    except Exception as e:
        # Fallback to rule-based recipe narration if API fails
        title = recipe.get("title", "Delicious Dish")
        tags = recipe.get("tags", [])
        
        title_lower = title.lower()
        if "biryani" in title_lower:
            emoji = "🍛"
            cooking_time = "40–50 mins"
            difficulty = "⭐⭐⭐ Hard"
            description = "A rich, fragrant Biryani cooked with premium basmati rice, tender elements, aromatic spices, and warm ghee."
        elif "pulao" in title_lower:
            emoji = "🍛"
            cooking_time = "25–30 mins"
            difficulty = "⭐⭐ Medium"
            description = "A fragrant, spiced vegetarian rice dish cooked gently in ghee with aromatic herbs."
        elif "fried rice" in title_lower:
            emoji = "🍚"
            cooking_time = "10–15 mins"
            difficulty = "⭐ Easy"
            description = "A classic stir-fried rice tossed with veggies, seasonings, and soy sauce on high heat."
        elif "pasta" in title_lower:
            emoji = "🍝"
            cooking_time = "15–20 mins"
            difficulty = "⭐⭐ Medium"
            description = "A delightful, comforting pasta dish cooked to perfection with flavorful seasoning and fresh ingredients."
        elif "rice" in title_lower:
            emoji = "🍛"
            cooking_time = "20–30 mins"
            difficulty = "⭐⭐ Medium"
            description = "A wholesome, filling rice bowl packed with vibrant veggies and savory elements."
        elif "salad" in title_lower:
            emoji = "🥗"
            cooking_time = "10–15 mins"
            difficulty = "⭐ Easy"
            description = "A crisp, refreshing garden salad tossed in a light olive oil dressing, perfect as a healthy meal or side."
        elif "sandwich" in title_lower:
            emoji = "🥪"
            cooking_time = "5–10 mins"
            difficulty = "⭐ Easy"
            description = "A fresh, crisp sandwich layered with ingredients between perfectly toasted bread."
        elif "omelette" in title_lower:
            emoji = "🍳"
            cooking_time = "5–10 mins"
            difficulty = "⭐ Easy"
            description = "A fluffy, golden omelette folded with flavorful ingredients, perfect for breakfast or a quick snack."
        elif "soup" in title_lower:
            emoji = "🥣"
            cooking_time = "15–20 mins"
            difficulty = "⭐ Easy"
            description = "A warm, soothing homemade soup simmering with rich flavors and tender ingredients."
        elif "stir-fry" in title_lower:
            emoji = "🥢"
            cooking_time = "10–15 mins"
            difficulty = "⭐⭐ Medium"
            description = "A vibrant, sizzling stir-fry tossed in a flavorful sauce and cooked over high heat."
        else:
            emoji = "🍳"
            cooking_time = "20–30 mins"
            difficulty = "⭐ Easy"
            description = "A quick, pan-seared mixture of delicious ingredients seasoned to taste."
            
        display_title = f"Chef's Special {title} {emoji}"
        
        step_emojis = ["🔪", "🔥", "🍽️", "✨", "⭐"]
        original_steps = recipe.get("steps", [])
        narrated_steps = []
        
        for idx, step in enumerate(original_steps):
            prefix = step_emojis[idx] if idx < len(step_emojis) else "⭐"
            # Strip existing emojis if present to avoid doubling
            step_clean = step
            parts = step.split(" ", 1)
            if len(parts) > 1 and len(parts[0]) <= 2:
                step_clean = parts[1]
            narrated_steps.append(f"{prefix} {step_clean}")
            
        note = "Bon appétit! Made with love and your favorite ingredients. Enjoy your homemade creation! ❤️"
        
        return {
            "display_title": display_title,
            "ingredients": recipe.get("ingredients", []),
            "steps": narrated_steps,
            "servings": recipe.get("servings", 2),
            "tags": tags,
            "note": note,
            "cooking_time": cooking_time,
            "difficulty": difficulty,
            "description": description
        }
