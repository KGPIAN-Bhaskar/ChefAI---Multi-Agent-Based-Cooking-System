def narrate_recipe(recipe: dict) -> dict:
    """Add emojis, customized titles, and cheerful notes to make the recipe fun and engaging."""
    title = recipe.get("title", "Delicious Dish")
    tags = recipe.get("tags", [])
    
    # Estimate metadata and description based on recipe type
    title_lower = title.lower()
    if "pasta" in title_lower:
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
    else:
        emoji = "🍳"
        cooking_time = "20–30 mins"
        difficulty = "⭐ Easy"
        description = "A quick, pan-seared mixture of delicious seasonal veggies seasoned to taste."
        
    display_title = f"Chef's Special {title} {emoji}"
    
    # Emojis for each step
    step_emojis = ["🔪", "🔥", "🍽️", "✨"]
    original_steps = recipe.get("steps", [])
    narrated_steps = []
    
    for idx, step in enumerate(original_steps):
        prefix = step_emojis[idx] if idx < len(step_emojis) else "⭐"
        narrated_steps.append(f"{prefix} {step}")
        
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
