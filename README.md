<<<<<<< HEAD
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
=======


## 📌 Overview

Chef AI is an intelligent recipe generation system designed to simplify everyday cooking. Users can enter ingredients manually or upload ingredient files, and the application automatically generates personalized recipes with cooking instructions, preparation tips, and engaging narration.

The project demonstrates modular software design by separating responsibilities into independent components responsible for parsing, validation, recipe generation, orchestration, and presentation.

---

# ✨ Features

* 🥗 Generate recipes from available ingredients
* 📄 Upload ingredient files (`.txt` or `.json`)
* 🧹 Automatic ingredient cleaning and normalization
* 🔒 Secure input validation and sanitization
* 🍅 Duplicate removal and plural normalization
* 🍝 Intelligent rule-based recipe generation
* 🎭 Fun recipe narration with emojis
* 🎨 Modern and responsive Streamlit interface
* ⚡ Lightweight and beginner-friendly architecture
* 🔧 Modular Python codebase for easy extension

---

# 🚀 Tech Stack

| Technology    | Purpose           |
| ------------- | ----------------- |
| Python        | Core Programming  |
| Streamlit     | Web Interface     |
| JSON          | Data Handling     |
| Rule-Based AI | Recipe Generation |
| Git & GitHub  | Version Control   |

---

# 📂 Project Structure

```text
ChefAI-MultiAgent-Cooking-System/
│
<<<<<<< HEAD
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
=======
├── app.py                     # Streamlit User Interface
├── mcp_server.py              # Multi-Agent Orchestrator
├── recipe_generator.py        # Recipe Generation Logic
├── ingredient_parser.py       # Ingredient Parsing & Cleaning
├── narrator.py                # Recipe Narration
├── security.py                # Input Validation & Security
├── requirements.txt           # Project Dependencies
├── sample_ingredients.txt     # Sample Input
├── README.md                  # Documentation
└── .gitignore
>>>>>>> e31f6a4de592f36012adfd3a327a83caecd301eb
```

---

<<<<<<< HEAD
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
=======
# 🏗️ System Architecture

```text
                 User Input
                     │
          ┌──────────▼──────────┐
          │   Streamlit UI       │
          └──────────┬──────────┘
                     │
             Security Validation
                     │
                     ▼
         Ingredient Parser Agent
                     │
                     ▼
        Recipe Generator Agent
                     │
                     ▼
          Narrator / Formatter
                     │
                     ▼
            Final Recipe Card
```

---

# ⚙️ Workflow

### Step 1
>>>>>>> e31f6a4de592f36012adfd3a327a83caecd301eb

User enters ingredients or uploads a file.

### Step 2

Security module validates and sanitizes the input.

### Step 3

Parser extracts ingredients, removes duplicates, and normalizes plural words.

### Step 4

Recipe Generator creates a suitable recipe based on detected ingredients.

### Step 5

Narrator formats the recipe into a visually appealing cooking guide.

---

# 📦 Installation

Clone the repository:

```bash
git clone https://github.com/KGPIAN-Bhaskar/ChefAI-MultiAgent-Cooking-System.git
```

Move into the project directory:

```bash
cd ChefAI-MultiAgent-Cooking-System
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# ▶️ Run the Application

```bash
streamlit run app.py
```

<<<<<<< HEAD
---

## Sample Input
=======
The application will launch automatically in your default browser.
>>>>>>> e31f6a4de592f36012adfd3a327a83caecd301eb

---

# 📥 Sample Input

Example ingredient list:

```text
tomato
onion
garlic
olive oil
pasta
```

or JSON format

```json
[
<<<<<<< HEAD
  "chicken",
  "rice",
  "ghee"
=======
  "tomato",
  "onion",
  "garlic",
  "olive oil",
  "pasta"
>>>>>>> e31f6a4de592f36012adfd3a327a83caecd301eb
]
```

---

# 📊 Example Output

```
🍝 Garlic Tomato Pasta

Ingredients:
• Tomato
• Onion
• Garlic
• Pasta
• Olive Oil

Cooking Steps:
1. Heat olive oil.
2. Sauté onions and garlic.
3. Add chopped tomatoes.
4. Cook the pasta separately.
5. Mix everything together.
6. Garnish and serve hot.

Enjoy your meal! 🍽️
```

---

# 🔒 Security Features

* Input sanitization
* HTML tag removal
* Safe file upload validation
* Ingredient count validation
* Duplicate removal
* Invalid input detection

---

# 🎯 Future Improvements

* 🤖 LLM-powered recipe generation
* 🧠 Multi-Agent AI using LangGraph
* 🍎 Nutrition analysis
* 📸 Image-based ingredient recognition
* 🛒 Grocery recommendation system
* 🌍 Multi-language support
* 🎤 Voice-based cooking assistant
* 📱 Mobile application
* ☁️ Cloud deployment

---

# 🤝 Contributing

Contributions are welcome!

1. Fork this repository.
2. Create a new feature branch.
3. Commit your changes.
4. Submit a Pull Request.

---

# 📄 License

This project is intended for educational and learning purposes.

---

# 👨‍💻 Author

## **Bhaskar Mandal**

**AI/ML Engineer Enthusiast**

**M.Tech, IIT Kharagpur**

* 💼 Interested in Artificial Intelligence, Machine Learning, Data Science, and Multi-Agent Systems
* 🐍 Skilled in Python, C++, SQL, Machine Learning, Deep Learning, Streamlit, and Git
* 🌱 Currently exploring LLMs, RAG, LangChain, LangGraph, MCP, and AI Agents

### Connect with me

* GitHub: https://github.com/KGPIAN-Bhaskar
* LinkedIn: https://www.linkedin.com/in/bhaskar-mandal/

---

⭐ **If you found this project helpful, consider giving it a Star on GitHub!**
