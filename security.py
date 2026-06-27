import re

def is_allowed_file(filename: str) -> bool:
    """Return True only for .txt and .json files."""
    if not filename:
        return False
    lower_filename = filename.lower()
    return lower_filename.endswith('.txt') or lower_filename.endswith('.json')

def sanitize_text(text: str) -> str:
    """Remove HTML/script-like content and trim whitespace."""
    if not text:
        return ""
    # Strip HTML tags
    clean = re.sub(r'<[^>]*>', '', text)
    # Remove javascript: protocols to prevent script execution
    clean = re.sub(r'(?i)javascript:', '', clean)
    return clean.strip()

def validate_ingredient_list(items: list[str]) -> tuple[bool, str]:
    """Validate list of ingredients: non-empty, between 1 and 30 items."""
    if not items:
        return False, "At least 1 ingredient is required."
    
    if len(items) > 30:
        return False, "A maximum of 30 ingredients is allowed."
    
    for idx, item in enumerate(items):
        if not item or not isinstance(item, str) or not item.strip():
            return False, f"Ingredient at position {idx + 1} cannot be empty."
            
    return True, ""
