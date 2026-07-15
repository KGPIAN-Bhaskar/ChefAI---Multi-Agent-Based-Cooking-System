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

class RecipeOutput(BaseModel):
    title: str
    servings: int
    ingredients: list[str]
    steps: list[str]
    tags: list[str]

def generate_recipe(ingredients: list[str]) -> dict:
    """Use Gemini to dynamically generate a recipe title, tags, and exactly 5 instructions."""
    if not ingredients:
        return {
            "title": "Chef's Special Surprise",
            "servings": 2,
            "ingredients": [],
            "steps": ["Wait for ingredients...", "Prepare kitchen...", "Cook...", "Plate...", "Enjoy!"],
            "tags": ["quick", "easy"]
        }
        
    client = get_client()
    if client is None:
        # Fallback to rule-based recipe generation if API fails
        display_ingredients = [item.title() for item in ingredients]
        lower_ingredients = [item.lower() for item in ingredients]
        
        meat_keywords = {
            "chicken", "meat", "beef", "pork", "fish", "shrimp", "mutton", 
            "steak", "bacon", "turkey", "duck", "seafood", "prawn", 
            "crab", "ham", "sausage", "salmon", "tuna"
        }
        is_vegetarian = not any(kw in lower_ingredients for kw in meat_keywords)
        
        base_keywords = {
            "pasta", "rice", "lettuce", "cucumber", "bread", "toast", "bun", 
            "egg", "eggs", "water", "broth", "soup", "soy sauce", "ginger", 
            "garlic", "oil", "salt", "pepper", "ghee"
        }
        non_base = [item.title() for item in ingredients if item.lower() not in base_keywords]
        title_ingredient = non_base[0] if non_base else (display_ingredients[0] if display_ingredients else "Veggie")
        
        base_tags = ["quick", "easy"]
        if is_vegetarian:
            base_tags.append("vegetarian")
        else:
            base_tags.append("meat")
            
        has_rice = any(item in lower_ingredients for item in ["rice", "quinoa"])
        has_ghee = "ghee" in lower_ingredients
        has_meat = any(kw in lower_ingredients for kw in meat_keywords)
        has_soy_sauce = any(item in lower_ingredients for item in ["soy sauce", "soy", "sauce"])
        has_ginger_garlic = any(item in lower_ingredients for item in ["ginger", "garlic"])
        
        if has_rice and has_ghee and has_meat:
            title = f"{title_ingredient} Biryani"
            steps = [
                "Rinse the basmati rice and soak in water for 30 minutes, then half-boil it with whole spices.",
                "Heat ghee in a deep pot and sauté the onions, ginger-garlic paste, and meat until browned.",
                "Stir in the remaining ingredients, cover, and cook the meat mixture until tender.",
                "Layer the half-boiled rice over the cooked meat mixture, adding ghee and herbs on top.",
                "Seal the pot tightly with a lid and cook on very low heat (Dum) for 15-20 minutes."
            ]
            style_tag = "biryani"
        elif has_rice and has_ghee and is_vegetarian:
            title = f"{title_ingredient} Pulao"
            steps = [
                "Rinse the basmati rice thoroughly and soak in water for 20-30 minutes.",
                "Heat ghee in a pot and sauté spices like cumin, cardamom, and cinnamon.",
                "Toss in the vegetables and sauté for 2-3 minutes until lightly softened.",
                "Add the soaked rice and pour in warm water, bringing it to a boil.",
                "Cover tightly, reduce the heat, and simmer until all water is absorbed and rice is fluffy."
            ]
            style_tag = "pulao"
        elif has_rice and (has_soy_sauce or has_ginger_garlic or any(kw in lower_ingredients for kw in ["onion", "carrot", "pea", "corn", "vegetable"])):
            title = f"{title_ingredient} Fried Rice"
            steps = [
                "Cook the rice beforehand and let it cool completely (or use day-old cold rice).",
                "Heat cooking oil in a large wok over high heat until smoking.",
                "Sauté the chopped vegetables and meat/eggs in the wok until tender.",
                "Add the cold rice, breaking up any clumps, and toss continuously.",
                "Drizzle with soy sauce and sesame oil, stir-fry for 2 minutes on high heat, and serve hot."
            ]
            style_tag = "fried-rice"
        elif any(item in lower_ingredients for item in ["pasta", "noodles", "spaghetti"]):
            title = f"{title_ingredient} Pasta"
            steps = [
                "Cook the pasta in salted boiling water until al dente, drain it, and set aside.",
                "Heat cooking oil in a pan and sauté the garlic and onion until fragrant.",
                "Add the remaining ingredients and toss over medium heat for 5-6 minutes.",
                "Stir in the drained pasta, season with herbs/pepper, and mix well.",
                "Plate the pasta hot, garnish with cheese if available, and serve."
            ]
            style_tag = "pasta"
        elif any(item in lower_ingredients for item in ["bread", "toast", "bun"]):
            title = f"{title_ingredient} Sandwich"
            steps = [
                "Lightly toast your bread or buns until golden and crispy.",
                "Finely slice the other ingredients (like tomatoes, cheese, or meat).",
                "Spread butter, mayonnaise, or oil on the inner side of the toasted bread.",
                "Assemble the sliced ingredients in layers inside the bread slices.",
                "Slice the sandwich diagonally, plate, and serve immediately."
            ]
            style_tag = "sandwich"
        elif any(item in lower_ingredients for item in ["egg", "eggs"]):
            title = f"{title_ingredient} Omelette"
            steps = [
                "Crack the eggs into a bowl and whisk thoroughly with salt and pepper.",
                "Heat oil or ghee in a pan and cook the chopped meat or vegetables first.",
                "Pour the whisked egg mixture evenly over the cooked ingredients in the pan.",
                "Let the mixture cook on medium heat until the edges are set and golden.",
                "Fold the omelette in half, cook for 1 more minute, and slide onto a plate."
            ]
            style_tag = "omelette"
        elif any(item in lower_ingredients for item in ["soup", "broth", "water"]):
            title = f"Warm {title_ingredient} Soup"
            steps = [
                "Chop all the main ingredients into small, bite-sized pieces.",
                "Heat a cooking pot with a touch of oil or butter and sauté the aromatics.",
                "Pour in water or broth and bring the mixture to a rolling boil.",
                "Reduce the heat, cover the pot, and let it simmer for 15-20 minutes.",
                "Check seasoning, ladle the hot soup into a bowl, and serve."
            ]
            style_tag = "soup"
        elif any(item in lower_ingredients for item in ["soy sauce", "ginger"]):
            title = f"{title_ingredient} Stir-Fry"
            steps = [
                "Prep and slice the main ingredients into uniform, thin pieces.",
                "Heat a wok or large pan with oil over high heat until sizzling.",
                "Add the meat or hard vegetables first, tossing continuously for 3-4 minutes.",
                "Stir in the remaining soft ingredients, soy sauce, and aromatic ginger.",
                "Sauté on high heat for another 2 minutes until everything is evenly glazed."
            ]
            style_tag = "stir-fry"
        elif any(item in lower_ingredients for item in ["lettuce", "cucumber", "salad", "spinach"]):
            title = f"{title_ingredient} Fresh Salad"
            steps = [
                "Thoroughly wash the fresh lettuce, cucumber, and salad greens.",
                "Chop the ingredients into uniform slices or bite-sized cubes.",
                "Place the chopped ingredients in a large, clean salad bowl.",
                "Drizzle with olive oil, fresh lemon juice, salt, and pepper.",
                "Toss the salad gently to mix the dressing evenly, then serve chilled."
            ]
            style_tag = "salad"
        else:
            title = f"Mixed {title_ingredient} Skillet"
            steps = [
                "Chop all of the ingredients into uniform chunks or slices.",
                "Heat cooking oil in a skillet over medium-high heat.",
                "Sauté the ingredients in the skillet, starting with the denser items.",
                "Stir frequently for 8-10 minutes until everything is tender and cooked.",
                "Season to taste with salt, pepper, or herbs, and serve hot."
            ]
            style_tag = "skillet"
            
        tags = base_tags + [style_tag]
        return {
            "title": title,
            "servings": 2,
            "ingredients": display_ingredients,
            "steps": steps,
            "tags": tags
        }
        
    try:
        prompt = f"""
        You are the Master Chef Recipe Generator Agent for Chef AI. Take the following clean ingredient list:
        {", ".join(ingredients)}
        
        Perform the following tasks:
        1. Contextually decide the best recipe style to make using these ingredients (e.g., Biryani, Pulao, Fried Rice, Pasta, Sandwich, Omelette, Soup, Stir-Fry, or Skillet).
        2. Generate a creative title for the recipe (e.g. 'Chicken Biryani', 'Vegetable Pasta', 'Tomato Cheese Omelette'). Do NOT include prefixes like 'Chef\'s Special' - just return the raw title.
        3. Write exactly 5 logical, sequential, step-by-step cooking instructions. Ensure each step is a single clear action.
        4. Decide the servings size (default to 2).
        5. Build a list of tags including 'quick', 'easy', a classification ('vegetarian' or 'meat' - check if ingredients include chicken, meat, beef, fish, etc.), and the recipe style (e.g., 'biryani', 'pasta', 'pulao', 'fried-rice', 'sandwich', 'omelette', 'soup', 'stir-fry', 'skillet').
        
        Ensure your output matches the requested JSON schema.
        """
        
        response = client.models.generate_content(
            model='gemini-3.1-flash-lite',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=RecipeOutput,
                temperature=0.7
            )
        )
        
        result = json.loads(response.text)
        return {
            "title": result.get("title", "Delicious Meal").strip(),
            "servings": result.get("servings", 2),
            "ingredients": [i.title() for i in result.get("ingredients", ingredients)],
            "steps": result.get("steps", [])[:5],
            "tags": [t.lower() for t in result.get("tags", ["quick", "easy"])]
        }
    except Exception as e:
        # Fallback to rule-based recipe generation if API fails
        display_ingredients = [item.title() for item in ingredients]
        lower_ingredients = [item.lower() for item in ingredients]
        
        meat_keywords = {
            "chicken", "meat", "beef", "pork", "fish", "shrimp", "mutton", 
            "steak", "bacon", "turkey", "duck", "seafood", "prawn", 
            "crab", "ham", "sausage", "salmon", "tuna"
        }
        is_vegetarian = not any(kw in lower_ingredients for kw in meat_keywords)
        
        base_keywords = {
            "pasta", "rice", "lettuce", "cucumber", "bread", "toast", "bun", 
            "egg", "eggs", "water", "broth", "soup", "soy sauce", "ginger", 
            "garlic", "oil", "salt", "pepper", "ghee"
        }
        non_base = [item.title() for item in ingredients if item.lower() not in base_keywords]
        title_ingredient = non_base[0] if non_base else (display_ingredients[0] if display_ingredients else "Veggie")
        
        base_tags = ["quick", "easy"]
        if is_vegetarian:
            base_tags.append("vegetarian")
        else:
            base_tags.append("meat")
            
        has_rice = any(item in lower_ingredients for item in ["rice", "quinoa"])
        has_ghee = "ghee" in lower_ingredients
        has_meat = any(kw in lower_ingredients for kw in meat_keywords)
        has_soy_sauce = any(item in lower_ingredients for item in ["soy sauce", "soy", "sauce"])
        has_ginger_garlic = any(item in lower_ingredients for item in ["ginger", "garlic"])
        
        if has_rice and has_ghee and has_meat:
            title = f"{title_ingredient} Biryani"
            steps = [
                "Rinse the basmati rice and soak in water for 30 minutes, then half-boil it with whole spices.",
                "Heat ghee in a deep pot and sauté the onions, ginger-garlic paste, and meat until browned.",
                "Stir in the remaining ingredients, cover, and cook the meat mixture until tender.",
                "Layer the half-boiled rice over the cooked meat mixture, adding ghee and herbs on top.",
                "Seal the pot tightly with a lid and cook on very low heat (Dum) for 15-20 minutes."
            ]
            style_tag = "biryani"
        elif has_rice and has_ghee and is_vegetarian:
            title = f"{title_ingredient} Pulao"
            steps = [
                "Rinse the basmati rice thoroughly and soak in water for 20-30 minutes.",
                "Heat ghee in a pot and sauté spices like cumin, cardamom, and cinnamon.",
                "Toss in the vegetables and sauté for 2-3 minutes until lightly softened.",
                "Add the soaked rice and pour in warm water, bringing it to a boil.",
                "Cover tightly, reduce the heat, and simmer until all water is absorbed and rice is fluffy."
            ]
            style_tag = "pulao"
        elif has_rice and (has_soy_sauce or has_ginger_garlic or any(kw in lower_ingredients for kw in ["onion", "carrot", "pea", "corn", "vegetable"])):
            title = f"{title_ingredient} Fried Rice"
            steps = [
                "Cook the rice beforehand and let it cool completely (or use day-old cold rice).",
                "Heat cooking oil in a large wok over high heat until smoking.",
                "Sauté the chopped vegetables and meat/eggs in the wok until tender.",
                "Add the cold rice, breaking up any clumps, and toss continuously.",
                "Drizzle with soy sauce and sesame oil, stir-fry for 2 minutes on high heat, and serve hot."
            ]
            style_tag = "fried-rice"
        elif any(item in lower_ingredients for item in ["pasta", "noodles", "spaghetti"]):
            title = f"{title_ingredient} Pasta"
            steps = [
                "Cook the pasta in salted boiling water until al dente, drain it, and set aside.",
                "Heat cooking oil in a pan and sauté the garlic and onion until fragrant.",
                "Add the remaining ingredients and toss over medium heat for 5-6 minutes.",
                "Stir in the drained pasta, season with herbs/pepper, and mix well.",
                "Plate the pasta hot, garnish with cheese if available, and serve."
            ]
            style_tag = "pasta"
        elif any(item in lower_ingredients for item in ["bread", "toast", "bun"]):
            title = f"{title_ingredient} Sandwich"
            steps = [
                "Lightly toast your bread or buns until golden and crispy.",
                "Finely slice the other ingredients (like tomatoes, cheese, or meat).",
                "Spread butter, mayonnaise, or oil on the inner side of the toasted bread.",
                "Assemble the sliced ingredients in layers inside the bread slices.",
                "Slice the sandwich diagonally, plate, and serve immediately."
            ]
            style_tag = "sandwich"
        elif any(item in lower_ingredients for item in ["egg", "eggs"]):
            title = f"{title_ingredient} Omelette"
            steps = [
                "Crack the eggs into a bowl and whisk thoroughly with salt and pepper.",
                "Heat oil or ghee in a pan and cook the chopped meat or vegetables first.",
                "Pour the whisked egg mixture evenly over the cooked ingredients in the pan.",
                "Let the mixture cook on medium heat until the edges are set and golden.",
                "Fold the omelette in half, cook for 1 more minute, and slide onto a plate."
            ]
            style_tag = "omelette"
        elif any(item in lower_ingredients for item in ["soup", "broth", "water"]):
            title = f"Warm {title_ingredient} Soup"
            steps = [
                "Chop all the main ingredients into small, bite-sized pieces.",
                "Heat a cooking pot with a touch of oil or butter and sauté the aromatics.",
                "Pour in water or broth and bring the mixture to a rolling boil.",
                "Reduce the heat, cover the pot, and let it simmer for 15-20 minutes.",
                "Check seasoning, ladle the hot soup into a bowl, and serve."
            ]
            style_tag = "soup"
        elif any(item in lower_ingredients for item in ["soy sauce", "ginger"]):
            title = f"{title_ingredient} Stir-Fry"
            steps = [
                "Prep and slice the main ingredients into uniform, thin pieces.",
                "Heat a wok or large pan with oil over high heat until sizzling.",
                "Add the meat or hard vegetables first, tossing continuously for 3-4 minutes.",
                "Stir in the remaining soft ingredients, soy sauce, and aromatic ginger.",
                "Sauté on high heat for another 2 minutes until everything is evenly glazed."
            ]
            style_tag = "stir-fry"
        elif any(item in lower_ingredients for item in ["lettuce", "cucumber", "salad", "spinach"]):
            title = f"{title_ingredient} Fresh Salad"
            steps = [
                "Thoroughly wash the fresh lettuce, cucumber, and salad greens.",
                "Chop the ingredients into uniform slices or bite-sized cubes.",
                "Place the chopped ingredients in a large, clean salad bowl.",
                "Drizzle with olive oil, fresh lemon juice, salt, and pepper.",
                "Toss the salad gently to mix the dressing evenly, then serve chilled."
            ]
            style_tag = "salad"
        else:
            title = f"Mixed {title_ingredient} Skillet"
            steps = [
                "Chop all of the ingredients into uniform chunks or slices.",
                "Heat cooking oil in a skillet over medium-high heat.",
                "Sauté the ingredients in the skillet, starting with the denser items.",
                "Stir frequently for 8-10 minutes until everything is tender and cooked.",
                "Season to taste with salt, pepper, or herbs, and serve hot."
            ]
            style_tag = "skillet"
            
        tags = base_tags + [style_tag]
        return {
            "title": title,
            "servings": 2,
            "ingredients": display_ingredients,
            "steps": steps,
            "tags": tags
        }
