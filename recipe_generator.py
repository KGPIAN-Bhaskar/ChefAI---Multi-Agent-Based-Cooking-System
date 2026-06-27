def generate_recipe(ingredients: list[str]) -> dict:
    """Generate a recipe dictionary using simple rule-based logic based on available ingredients."""
    # Format ingredients for display
    display_ingredients = [item.title() for item in ingredients]
    lower_ingredients = [item.lower() for item in ingredients]
    
    # Choose a key ingredient to name the recipe
    base_keywords = {"pasta", "rice", "lettuce", "cucumber"}
    non_base = [item.title() for item in ingredients if item.lower() not in base_keywords]
    title_ingredient = non_base[0] if non_base else (display_ingredients[0] if display_ingredients else "Veggie")
    
    # Default tags
    default_tags = ["quick", "vegetarian", "easy"]
    
    if "pasta" in lower_ingredients:
        title = f"{title_ingredient} Pasta"
        steps = [
            "Cook the pasta in salted boiling water until tender, then drain and set aside.",
            "In a pan, cook the other ingredients with oil and spices until aromatic.",
            "Toss the pasta with the mixture, stirring well over low heat, and serve."
        ]
        tags = default_tags + ["pasta"]
    elif "rice" in lower_ingredients:
        title = f"{title_ingredient} Rice Bowl"
        steps = [
            "Prepare the rice until fully cooked and fluffy.",
            "Saute the rest of the ingredients in a pan with seasoning until warm and cooked.",
            "Place rice in a bowl and spoon the cooked ingredients over the top."
        ]
        tags = default_tags + ["rice"]
    elif "lettuce" in lower_ingredients or "cucumber" in lower_ingredients:
        title = f"{title_ingredient} Fresh Salad"
        steps = [
            "Wash all the fresh ingredients thoroughly.",
            "Chop the ingredients into thin slices or bite-sized cubes.",
            "Combine in a bowl, season with salt, pepper, olive oil, and toss gently."
        ]
        tags = default_tags + ["salad"]
    else:
        title = f"Mixed {title_ingredient} Skillet"
        steps = [
            "Wash and slice the ingredients into uniform pieces.",
            "Heat cooking oil in a skillet and cook the ingredients over medium heat.",
            "Stir frequently for 8-10 minutes until tender, then season to taste."
        ]
        tags = default_tags + ["skillet"]

    return {
        "title": title,
        "servings": 2,
        "ingredients": display_ingredients,
        "steps": steps,
        "tags": tags
    }
