# 👨‍🍳 Chef AI – Multi-Agent Cooking System

> **An AI-powered multi-agent cooking assistant that transforms everyday ingredients into delicious recipes using intelligent agent-based workflows and a modern Streamlit interface.**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Web%20App-red)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)

---

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
```

---

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

The application will launch automatically in your default browser.

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
  "tomato",
  "onion",
  "garlic",
  "olive oil",
  "pasta"
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
