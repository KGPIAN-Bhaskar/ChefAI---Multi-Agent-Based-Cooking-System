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

class ParserOutput(BaseModel):
    ingredients: list[str]

def parse_ingredients(raw_text: str) -> list[str]:
    """Use Gemini to parse, clean, correct spelling typos, normalize plurals, and deduplicate ingredients."""
    if not raw_text or not raw_text.strip():
        return []
        
    client = get_client()
    if client is None:
        # Fallback to rule-based parsing if API fails
        normalized_text = raw_text.replace('\n', ',')
        parts = normalized_text.split(',')
        parsed = []
        seen = set()
        
        # Plural & typo map fallback
        fallback_map = {
            "tomatoes": "tomato", "potatoes": "potato", "onions": "onion", "carrots": "carrot",
            "chiken": "chicken", "o ui": "oil", "gee": "ghee", "veg": "vegetable",
            "veggie": "vegetable", "veggies": "vegetable"
        }
        for part in parts:
            clean_part = part.strip().lower()
            if not clean_part:
                continue
            if clean_part in fallback_map:
                clean_part = fallback_map[clean_part]
            if clean_part not in seen:
                seen.add(clean_part)
                parsed.append(clean_part)
        return parsed
        
    try:
        prompt = f"""
        You are the Parser Agent for Chef AI. Take the following raw ingredient input:
        ---
        {raw_text}
        ---
        
        Perform the following tasks:
        1. Split the inputs by commas, newlines, or other logical boundaries.
        2. Clean and trim whitespace, and convert all ingredients to lowercase.
        3. Correct common spelling typos (e.g. 'chiken' -> 'chicken', 'o ui' -> 'oil', 'gee' -> 'ghee', etc.).
        4. Normalize plurals to singular forms (e.g. 'tomatoes' -> 'tomato', 'onions' -> 'onion', 'potatoes' -> 'potato', etc.).
        5. Remove duplicate ingredients.
        
        Return the final list of clean, normalized, unique ingredients.
        """
        
        response = client.models.generate_content(
            model='gemini-3.1-flash-lite',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ParserOutput,
                temperature=0.0
            )
        )
        
        result = json.loads(response.text)
        return [i.strip().lower() for i in result.get("ingredients", []) if i.strip()]
    except Exception as e:
        # Fallback to rule-based parsing if API fails
        normalized_text = raw_text.replace('\n', ',')
        parts = normalized_text.split(',')
        parsed = []
        seen = set()
        
        # Plural & typo map fallback
        fallback_map = {
            "tomatoes": "tomato", "potatoes": "potato", "onions": "onion", "carrots": "carrot",
            "chiken": "chicken", "o ui": "oil", "gee": "ghee", "veg": "vegetable",
            "veggie": "vegetable", "veggies": "vegetable"
        }
        for part in parts:
            clean_part = part.strip().lower()
            if not clean_part:
                continue
            if clean_part in fallback_map:
                clean_part = fallback_map[clean_part]
            if clean_part not in seen:
                seen.add(clean_part)
                parsed.append(clean_part)
        return parsed
