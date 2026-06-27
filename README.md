# Chef AI – Ingredient to Recipe

A beginner-friendly Streamlit web application that takes raw text or file inputs of ingredients and generates a fun recipe card dynamically based on rule-based logic.

## Features

- **Text & File Input**: Input ingredients directly or upload a `.txt` or `.json` file.
- **Input Sanitization & Validation**: Ensures safe, clean, and valid ingredient counts (between 1 and 30).
- **Plural Normalization**: Automatically converts plurals like `tomatoes` to `tomato` and removes duplicates.
- **Rule-based Generation**: Generates customized recipe styles (Pasta, Rice Bowl, Salad, or Skillet) based on key ingredients.
- **Cheerful Narration**: Enriches recipes with fun display titles, step-by-step emojis, and cute notes.
- **Premium UI**: Modern layout featuring floating food emoji animations.

## File Structure

```
chef-ai-recipe-generator/
│
├── app.py                  # Streamlit UI
├── mcp_server.py           # Orchestration module
├── recipe_generator.py     # Rule-based recipe generator
├── ingredient_parser.py    # Ingredient text parsing and normalization
├── narrator.py             # Recipe narrator with emojis and titles
├── security.py             # Security checks, sanitization, and validations
├── requirements.txt        # Project dependencies
├── README.md               # Project documentation
└── sample_ingredients.txt   # Sample ingredients list for testing
```

## Architecture

```
Streamlit UI -> Security -> Parser -> Generator -> Narrator
```

1. **Streamlit UI (`app.py`)**: Renders layout, handles user interaction, text input, and file upload.
2. **Security (`security.py`)**: Sanitizes inputs, removes HTML, checks file extensions, and validates list counts.
3. **Parser (`ingredient_parser.py`)**: Splits, cleans, normalizes simple plurals, and deduplicates inputs.
4. **Generator (`recipe_generator.py`)**: Evaluates ingredients to produce steps, title, and tags based on simple rules.
5. **Narrator (`narrator.py`)**: Decorates the output with cooking emojis and custom title stylings.

## Installation Instructions

1. Ensure Python 3.8+ is installed.
2. Open your terminal in the workspace directory.
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run

Launch the application using Streamlit:
```bash
streamlit run app.py
```

## Sample Input

You can test with the provided `sample_ingredients.txt` containing:
```
tomato
onion
pasta
garlic
olive oil
```
Or upload a JSON list file like:
```json
[
  "tomato",
  "onion",
  "pasta",
  "garlic",
  "olive oil"
]
```
