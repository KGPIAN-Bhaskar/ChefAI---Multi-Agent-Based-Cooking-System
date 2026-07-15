# Chef AI – LLM Multi-Agent Cooking System

Chef AI is a modern Streamlit web application powered by a cooperative **LLM Multi-Agent System** using the modern `google-genai` SDK and the `gemini-3.1-flash-lite` model. It takes raw text inputs or ingredient files and transforms them into beautifully narrated, step-by-step recipe cards.

---

## Architecture

The system coordinates 4 specialized LLM agents in a sequential, cooperative pipeline:

```
Streamlit UI ──> Security Agent ──> Parser Agent ──> Recipe Gen Agent ──> Narrator Agent
```

1. **Security Agent** ([security.py](file:///C:/Users/manda/Desktop/Chef%20AI/security.py)): Evaluates the raw input for safety issues (injections, script executions, vulgarity) and checks if the prompt is food-related.
2. **Parser Agent** ([ingredient_parser.py](file:///C:/Users/manda/Desktop/Chef%20AI/ingredient_parser.py)): Splits inputs, corrects typos (e.g. `chiken` $\rightarrow$ `chicken`), normalizes plurals to singular, and removes duplicates.
3. **Recipe Generator Agent** ([recipe_generator.py](file:///C:/Users/manda/Desktop/Chef%20AI/recipe_generator.py)): Dynamically decides a cooking style based on ingredients and writes exactly 5 clear, sequential cooking instructions.
4. **Narrator Agent** ([narrator.py](file:///C:/Users/manda/Desktop/Chef%20AI/narrator.py)): Decorates the steps with stage-specific cooking emojis, writes descriptions, adds friendly chef notes, and computes servings/cooking time.

---

## Features

- **Cooperative LLM Multi-Agent System**: Utilizes `gemini-3.1-flash-lite` for advanced reasoning, spelling correction, safety, and cooking narration.
- **Strict 4-Call Production Limit**: Generates every recipe using exactly 4 total LLM calls (1 call per agent) to preserve API quota on the free tier.
- **Zero-Error Fallback Security**: Built-in offline mode. If `GEMINI_API_KEY` is not present, all agents degrade to a localized, rule-based algorithm automatically.
- **Modern UI**: Streamlit interface with floating animated food emojis.

---

## File Structure

```
chef-ai-recipe-generator/
│
├── app.py                  # Streamlit UI
├── mcp_server.py           # Orchestration module
├── security.py             # Security checks, sanitization, and Pydantic schemas
├── ingredient_parser.py    # Typo correction, plural normalization, and parser schemas
├── recipe_generator.py     # Recipe generation and selector schemas
├── narrator.py             # Recipe narrator, metadata compiler, and decorator schemas
│
├── .env                    # Local environment variables (ignored by git)
├── .gitignore              # Git ignore rules
├── requirements.txt        # Project dependencies
├── README.md               # Project documentation
└── sample_ingredients.txt   # Sample ingredients list for testing
```

---

## Installation & Setup

1. Ensure Python 3.8+ is installed.
2. Clone this workspace directory.
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the root directory and add your Gemini API Key:
   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   ```

---

## How to Run

Launch the application using Streamlit:
```bash
streamlit run app.py
```

---

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
  "chicken",
  "rice",
  "ghee"
]
```
