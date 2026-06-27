def parse_ingredients(raw_text: str) -> list[str]:
    """Split by commas and newlines, convert to lowercase, normalize plurals, and remove duplicates."""
    if not raw_text:
        return []
    
    # Standardize delimiters by converting newlines to commas
    normalized_text = raw_text.replace('\n', ',')
    parts = normalized_text.split(',')
    
    parsed = []
    seen = set()
    
    # Plural normalization mappings
    plural_map = {
        "tomatoes": "tomato",
        "potatoes": "potato",
        "onions": "onion",
        "carrots": "carrot"
    }
    
    for part in parts:
        clean_part = part.strip().lower()
        if not clean_part:
            continue
        
        # Apply plural normalization
        if clean_part in plural_map:
            clean_part = plural_map[clean_part]
            
        # Deduplicate while preserving order
        if clean_part not in seen:
            seen.add(clean_part)
            parsed.append(clean_part)
            
    return parsed
