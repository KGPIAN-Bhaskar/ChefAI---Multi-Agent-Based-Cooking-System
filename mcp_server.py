from security import sanitize_text, validate_ingredient_list
from ingredient_parser import parse_ingredients
from recipe_generator import generate_recipe
from narrator import narrate_recipe

def process_input(raw_text: str) -> dict:
    """Orchestrate sanitization, parsing, validation, generation, and narration of recipe."""
    # 1. Sanitize text
    sanitized = sanitize_text(raw_text)
    if not sanitized:
        raise ValueError("Input is empty or contains only invalid characters.")
        
    # 2. Parse ingredients
    ingredients = parse_ingredients(sanitized)
    
    # 3. Validate ingredients
    is_valid, error_msg = validate_ingredient_list(ingredients)
    if not is_valid:
        raise ValueError(error_msg)
        
    # 4. Generate recipe
    recipe = generate_recipe(ingredients)
    
    # 5. Narrate recipe
    narrated = narrate_recipe(recipe)
    
    return narrated
