
# pyrefly: ignore [missing-import]
import streamlit as st
import json
from mcp_server import process_input
from security import is_allowed_file

def clean_html(html_str: str) -> str:
    """Remove leading whitespace/indentation from each line to prevent Markdown code block interpretation."""
    if not html_str:
        return ""
    return "\n".join(line.strip() for line in html_str.split("\n"))


# Set up page configurations
st.set_page_config(
    page_title="Multi-Agent Based Cooking System",
    page_icon="🍳",
    layout="wide"
)

# Modern UI Styling organized into clean sections
css_styles = """
<style>
/* ==========================================
   1. FONTS & RESET
   ========================================== */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"], .stText, .stMarkdown, .stButton, .stTextArea, .stFileUploader, .stRadio {
    font-family: 'Poppins', sans-serif !important;
}

/* ==========================================
   2. HIDE DEFAULT STREAMLIT MENU & FOOTER
   ========================================== */
header {visibility: hidden;}
footer {visibility: hidden;}
#MainMenu {visibility: hidden;}
.stDeployButton {display: none;}

/* ==========================================
   3. BACKGROUND & GLOBAL COLORS
   ========================================== */
.stApp {
    background-color: #F8FAFC !important;
    color: #1F2937 !important;
}

/* ==========================================
   4. HERO HEADER SECTION
   ========================================== */
.hero-section {
    background: linear-gradient(135deg, #E2F9F6 0%, #FFFBEB 100%);
    padding: 45px 30px;
    border-radius: 20px;
    box-shadow: 0 10px 25px -5px rgba(20, 184, 166, 0.1), 0 8px 10px -6px rgba(20, 184, 166, 0.05);
    text-align: center;
    margin-bottom: 35px;
    position: relative;
    border: 1px solid rgba(20, 184, 166, 0.15);
}

.hero-title {
    font-size: 48px;
    font-weight: 700;
    color: #1F2937;
    margin: 10px 0;
    text-align: center !important;
}

.hero-subtitle {
    font-size: 20px;
    color: #6B7280;
    max-width: 700px;
    margin: 0 auto;
    font-weight: 400;
    text-align: center !important;
}

/* Floating Emojis Anim */
.floating-container {
    display: flex;
    justify-content: center;
    gap: 18px;
    margin-bottom: 15px;
}

.float-emoji {
    display: inline-block;
    font-size: 2.5rem;
    animation: floatMove 3s ease-in-out infinite;
}
.float-emoji:nth-child(2) { animation-delay: 0.4s; animation-duration: 2.6s; }
.float-emoji:nth-child(3) { animation-delay: 0.8s; animation-duration: 3.2s; }
.float-emoji:nth-child(4) { animation-delay: 1.2s; animation-duration: 2.8s; }
.float-emoji:nth-child(5) { animation-delay: 1.6s; animation-duration: 3.4s; }
.float-emoji:nth-child(6) { animation-delay: 2s;   animation-duration: 3s; }

@keyframes floatMove {
    0% { transform: translateY(0px) rotate(0deg); }
    50% { transform: translateY(-15px) rotate(6deg); }
    100% { transform: translateY(0px) rotate(0deg); }
}

/* ==========================================
   5. INPUT CARD & WIDGET OVERRIDES
   ========================================== */
.form-card {
    background-color: #FFFFFF;
    border-radius: 16px;
    padding: 28px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
    border: 1px solid #E2E8F0;
    margin-bottom: 24px;
}

/* Custom styles for Streamlit components to blend with modern card theme */
div[data-baseweb="textarea"] {
    border-radius: 12px !important;
    border: 1px solid #CBD5E1 !important;
    transition: all 0.3s ease;
}
div[data-baseweb="textarea"]:focus-within {
    border-color: #14B8A6 !important;
    box-shadow: 0 0 0 3px rgba(20, 184, 166, 0.15) !important;
}

/* ==========================================
   6. MODERN GRADIENT BUTTONS & MICRO-ANIMATIONS
   ========================================== */
div.stButton > button {
    background: linear-gradient(135deg, #14B8A6 0%, #0D9488 100%) !important;
    color: white !important;
    border-radius: 12px !important;
    border: none !important;
    padding: 12px 28px !important;
    font-weight: 600 !important;
    font-size: 16px !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 6px -1px rgba(20, 184, 166, 0.2), 0 2px 4px -1px rgba(20, 184, 166, 0.1) !important;
    width: 100% !important;
    margin-top: 10px;
}
div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 15px -3px rgba(20, 184, 166, 0.3), 0 4px 6px -4px rgba(20, 184, 166, 0.2) !important;
}
div.stButton > button:active {
    transform: translateY(0);
}

/* ==========================================
   7. RECIPE CARD CONTAINER & FADE-IN
   ========================================== */
.recipe-card {
    background-color: #FFFFFF;
    border-radius: 18px;
    box-shadow: 0 15px 30px -10px rgba(0,0,0,0.06), 0 10px 15px -5px rgba(0,0,0,0.03);
    border: 1px solid #E2E8F0;
    overflow: hidden;
    animation: fadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

/* ==========================================
   8. PLACEHOLDER HERO IMAGE
   ========================================== */
.recipe-hero-image {
    height: 250px;
    background: linear-gradient(135deg, #14B8A6 0%, #0284C7 100%);
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    border-bottom: 1px solid #E2E8F0;
}
.recipe-hero-image.pasta {
    background: linear-gradient(135deg, #F59E0B 0%, #EA580C 100%);
}
.recipe-hero-image.rice {
    background: linear-gradient(135deg, #10B981 0%, #059669 100%);
}
.recipe-hero-image.salad {
    background: linear-gradient(135deg, #84CC16 0%, #16A34A 100%);
}
.recipe-hero-image.skillet {
    background: linear-gradient(135deg, #EC4899 0%, #D946EF 100%);
}

.recipe-image-emoji {
    font-size: 5.5rem;
    filter: drop-shadow(0 12px 10px rgba(0,0,0,0.18));
    animation: pulse 4s ease-in-out infinite;
}

@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.06); }
    100% { transform: scale(1); }
}

.recipe-content {
    padding: 35px;
}

.recipe-title-main {
    font-size: 28px;
    font-weight: 700;
    color: #1F2937;
    margin-bottom: 8px;
}

.recipe-description {
    font-size: 16px;
    color: #4B5563;
    margin-bottom: 25px;
    line-height: 1.6;
}

/* ==========================================
   9. META INFORMATION ROW & CARDS
   ========================================== */
.meta-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 30px;
}

@media (max-width: 768px) {
    .meta-row {
        grid-template-columns: repeat(2, 1fr);
    }
}

.meta-card {
    background-color: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 16px;
    text-align: center;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.meta-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 12px -3px rgba(0,0,0,0.05);
    border-color: #14B8A6;
}

.meta-label {
    font-size: 12px;
    color: #6B7280;
    font-weight: 600;
    margin-bottom: 6px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.meta-value {
    font-size: 15px;
    color: #1F2937;
    font-weight: 700;
}

/* ==========================================
   10. INGREDIENT CHIPS & BADGES
   ========================================== */
.chips-container {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 30px;
}

.ingredient-chip {
    display: inline-flex;
    align-items: center;
    background-color: #E2F9F6;
    color: #0F766E;
    padding: 8px 18px;
    border-radius: 24px;
    font-size: 14px;
    font-weight: 500;
    border: 1px solid #CCFBF1;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: default;
}

.ingredient-chip:hover {
    transform: scale(1.05);
    background-color: #CCFBF1;
    box-shadow: 0 4px 10px -2px rgba(20, 184, 166, 0.15);
}

/* ==========================================
   11. STEP CARDS SYSTEM
   ========================================== */
.steps-container {
    display: flex;
    flex-direction: column;
    gap: 16px;
    margin-bottom: 30px;
}

.step-card {
    display: flex;
    align-items: flex-start;
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 20px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.step-card:hover {
    border-color: #14B8A6;
    background-color: #F8FAFC;
    transform: translateX(6px);
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);
}

.step-number {
    background-color: #14B8A6;
    color: white;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    font-weight: 700;
    font-size: 14px;
    margin-right: 18px;
    flex-shrink: 0;
    box-shadow: 0 3px 5px rgba(20, 184, 166, 0.2);
}

.step-text {
    font-size: 15px;
    color: #1F2937;
    line-height: 1.6;
}

/* ==========================================
   12. CHEF'S TIP ACCENT BOX
   ========================================== */
.chef-tip-box {
    background-color: #FFFBEB;
    border-left: 5px solid #F59E0B;
    padding: 20px;
    border-radius: 12px;
    margin-top: 15px;
    border-top: 1px solid #FEF3C7;
    border-right: 1px solid #FEF3C7;
    border-bottom: 1px solid #FEF3C7;
}

.chef-tip-title {
    font-weight: 700;
    color: #B45309;
    margin-bottom: 6px;
    font-size: 15px;
    display: flex;
    align-items: center;
    gap: 6px;
}

.chef-tip-content {
    color: #78350F;
    font-size: 14.5px;
    line-height: 1.5;
}

/* ==========================================
   13. SUCCESS AND FADE IN BANNER
   ========================================== */
.success-banner {
    background-color: #ECFDF5;
    border: 1px solid #A7F3D0;
    color: #065F46;
    padding: 16px 20px;
    border-radius: 12px;
    margin-bottom: 24px;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 8px;
    box-shadow: 0 2px 4px rgba(6, 95, 70, 0.03);
    animation: fadeInUp 0.4s ease-out;
}

/* ==========================================
   14. WELCOME PLACEHOLDER DASHED CARD
   ========================================== */
.welcome-placeholder {
    background-color: #FFFFFF;
    border: 2px dashed #CBD5E1;
    border-radius: 18px;
    padding: 80px 24px;
    text-align: center;
    color: #64748B;
    height: 100%;
    min-height: 480px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);
}

.welcome-icon {
    font-size: 5rem;
    margin-bottom: 20px;
    animation: bounce 2s infinite ease-in-out;
}

@keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}

.welcome-title {
    font-size: 22px;
    font-weight: 600;
    color: #475569;
    margin-bottom: 8px;
}
</style>
"""
st.markdown(clean_html(css_styles), unsafe_allow_html=True)

# Helper Function: Choose an emoji for an ingredient
def get_ingredient_emoji(name: str) -> str:
    """Return an appropriate emoji for a given ingredient name."""
    name_lower = name.lower().strip()
    emoji_map = {
        "tomato": "🍅", "tomatoes": "🍅",
        "onion": "🧅", "onions": "🧅",
        "potato": "🥔", "potatoes": "🥔",
        "carrot": "🥕", "carrots": "🥕",
        "garlic": "🧄",
        "pasta": "🍝",
        "rice": "🍚", "rice bowl": "🍚",
        "lettuce": "🥬",
        "cucumber": "🥒",
        "olive oil": "🫒", "oil": "🛢️",
        "salt": "🧂",
        "pepper": "🌶️",
        "chicken": "🍗",
        "beef": "🥩",
        "meat": "🍖",
        "cheese": "🧀",
        "egg": "🥚", "eggs": "🥚",
        "milk": "🥛",
        "butter": "🧈",
        "bread": "🍞",
        "lemon": "🍋",
        "lime": "🍋",
        "herb": "🌿", "herbs": "🌿",
        "parsley": "🌿", "cilantro": "🌿",
        "mushroom": "🍄", "mushrooms": "🍄",
        "avocado": "🥑",
        "broccoli": "🥦",
        "spinach": "🥬",
        "cabbage": "🥬",
        "chili": "🌶️", "chilies": "🌶️",
        "fish": "🐟",
        "shrimp": "🍤",
        "bean": "🫘", "beans": "🫘",
        "sugar": "🍬",
        "flour": "🌾",
        "water": "💧",
        "wine": "🍷",
        "vinegar": "🍯",
        "honey": "🍯"
    }
    
    # Try exact match or partial match
    if name_lower in emoji_map:
        return emoji_map[name_lower]
        
    for key, val in emoji_map.items():
        if key in name_lower or name_lower in key:
            return val
            
    return "🥑"  # Fallback food emoji

# Helper Function: Generate tags HTML badges with different pastel colors
def get_tag_badge_html(tags: list[str]) -> str:
    """Generate pastel colored HTML badges for tags."""
    pastels = [
        ("background-color: #E0F2FE; color: #0369A1; border: 1px solid #BAE6FD;"),  # Blue
        ("background-color: #FEF3C7; color: #B45309; border: 1px solid #FDE68A;"),  # Amber
        ("background-color: #DCFCE7; color: #15803D; border: 1px solid #BBF7D0;"),  # Green
        ("background-color: #F3E8FF; color: #6B21A8; border: 1px solid #E9D5FF;"),  # Purple
        ("background-color: #FCE7F3; color: #BE185D; border: 1px solid #FBCFE8;"),  # Pink
        ("background-color: #FFE4E6; color: #B91C1C; border: 1px solid #FECDD3;"),  # Rose
    ]
    
    badges = []
    for i, tag in enumerate(tags):
        style = pastels[i % len(pastels)]
        badges.append(
            f'<span style="display: inline-block; padding: 4px 10px; border-radius: 8px; font-size: 11px; font-weight: 600; margin-right: 5px; margin-bottom: 5px; {style}">{tag.upper()}</span>'
        )
        
    return "".join(badges)

# Helper Function: Generate Difficulty Badge
def get_difficulty_badge_html(difficulty: str) -> str:
    """Generate HTML badge for difficulty."""
    if "Easy" in difficulty:
        style = "background-color: #DCFCE7; color: #15803D; border: 1px solid #BBF7D0;"
    elif "Medium" in difficulty:
        style = "background-color: #FEF3C7; color: #B45309; border: 1px solid #FDE68A;"
    else:
        style = "background-color: #FFE4E6; color: #B91C1C; border: 1px solid #FECDD3;"
        
    return f'<span style="display: inline-block; padding: 4px 12px; border-radius: 8px; font-size: 13px; font-weight: 600; {style}">{difficulty}</span>'

# Initialize session state for recipe
if "recipe" not in st.session_state:
    st.session_state.recipe = None

# Hero Header section
hero_html = """
<div class="hero-section">
    <div class="floating-container">
        <span class="float-emoji">🍅</span>
        <span class="float-emoji">🧅</span>
        <span class="float-emoji">🍝</span>
        <span class="float-emoji">🍗</span>
        <span class="float-emoji">🧄</span>
        <span class="float-emoji">🥬</span>
        <span class="float-emoji">🥑</span>
    </div>
    <h1 class="hero-title">Multi-Agent Based Cooking System</h1>
    
</div>
"""
st.markdown(clean_html(hero_html), unsafe_allow_html=True)

# Main Application Layout: Two columns for desktop, single column for mobile (automatically handled by st.columns)
left_col, right_col = st.columns([1, 1.2], gap="large")

with left_col:
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.subheader("👨‍🍳 Input Ingredients")
    
    input_mode = st.radio("Choose input method:", ["Type Ingredients", "Upload File"])
    
    raw_input_text = ""
    
    if input_mode == "Type Ingredients":
        raw_input_text = st.text_area(
            "Enter ingredients (separated by commas or new lines):",
            placeholder="tomato, onion, pasta, garlic, olive oil",
            height=180
        )
    else:
        uploaded_file = st.file_uploader(
            "Upload ingredient file (.txt or .json):",
            type=["txt", "json"]
        )
        if uploaded_file is not None:
            filename = uploaded_file.name
            if is_allowed_file(filename):
                try:
                    file_bytes = uploaded_file.read()
                    content_str = file_bytes.decode("utf-8")
                    
                    if filename.endswith(".json"):
                        try:
                            data = json.loads(content_str)
                            if isinstance(data, list):
                                raw_input_text = ", ".join(str(item) for item in data)
                            elif isinstance(data, dict):
                                ingredients_key = next((k for k in data.keys() if "ingredient" in k.lower()), None)
                                if ingredients_key and isinstance(data[ingredients_key], list):
                                    raw_input_text = ", ".join(str(item) for item in data[ingredients_key])
                                else:
                                    raw_input_text = ", ".join(str(v) for v in data.values())
                            else:
                                raw_input_text = str(data)
                        except json.JSONDecodeError:
                            st.warning("Could not parse file as JSON; reading as plain text.")
                            raw_input_text = content_str
                    else:
                        raw_input_text = content_str
                except Exception as e:
                    st.error(f"Error reading file: {e}")
            else:
                st.error("File type not allowed. Please upload only .txt or .json files.")

    generate_clicked = st.button("Generate Recipe", type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

    if generate_clicked:
        if not raw_input_text.strip():
            st.error("Please enter or upload ingredients first.")
        else:
            with st.spinner("Chef is preparing your recipe..."):
                try:
                    # Process using backend orchestration
                    recipe_card = process_input(raw_input_text)
                    st.session_state.recipe = recipe_card
                except ValueError as ve:
                    st.error(f"Validation Error: {ve}")
                    st.session_state.recipe = None
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")
                    st.session_state.recipe = None

with right_col:
    if st.session_state.recipe is not None:
        recipe = st.session_state.recipe
        
        # Determine image styles
        img_class = "skillet"
        img_emoji = "🍳"
        title_lower = recipe['display_title'].lower()
        if "pasta" in title_lower:
            img_class = "pasta"
            img_emoji = "🍝"
        elif "rice" in title_lower:
            img_class = "rice"
            img_emoji = "🍛"
        elif "salad" in title_lower:
            img_class = "salad"
            img_emoji = "🥗"
            
        # Compile chips HTML
        chips_html = '<div class="chips-container">'
        for ing in recipe['ingredients']:
            e_icon = get_ingredient_emoji(ing)
            chips_html += f'<span class="ingredient-chip">{e_icon} {ing}</span>'
        chips_html += '</div>'
        
        # Compile steps HTML
        steps_html = '<div class="steps-container">'
        for idx, step in enumerate(recipe['steps']):
            step_clean = step
            step_emoji = "🍲"
            parts = step.split(" ", 1)
            if len(parts) > 1 and len(parts[0]) <= 2:
                step_emoji = parts[0]
                step_clean = parts[1]
            steps_html += f"""
            <div class="step-card">
                <div class="step-number">{idx + 1}</div>
                <div class="step-text"><strong>{step_emoji}</strong> {step_clean}</div>
            </div>
            """
        steps_html += '</div>'
        
        # Badges HTML
        tag_badges = get_tag_badge_html(recipe['tags'])
        difficulty_badge = get_difficulty_badge_html(recipe.get('difficulty', '⭐ Easy'))
        
        # Success and Recipe layout
        success_banner = """
        <div class="success-banner">
            <span>✨</span> <strong>Recipe Prepared!</strong> Your custom recipe card is ready below.
        </div>
        """
        st.markdown(clean_html(success_banner), unsafe_allow_html=True)
        
        recipe_html = f"""
        <div class="recipe-card">
            <div class="recipe-hero-image {img_class}">
                <span class="recipe-image-emoji">{img_emoji}</span>
            </div>
            <div class="recipe-content">
                <h2 class="recipe-title-main">{recipe['display_title']}</h2>
                <p class="recipe-description">{recipe.get('description', 'A wonderful homemade dish prepared with fresh ingredients.')}</p>
                
                <div class="meta-row">
                    <div class="meta-card">
                        <div class="meta-label">⏱ Cooking Time</div>
                        <div class="meta-value">{recipe.get('cooking_time', '20–30 mins')}</div>
                    </div>
                    <div class="meta-card">
                        <div class="meta-label">👨‍🍳 Servings</div>
                        <div class="meta-value">{recipe['servings']} Servings</div>
                    </div>
                    <div class="meta-card">
                        <div class="meta-label">⭐ Difficulty</div>
                        <div class="meta-value" style="padding-top: 4px;">{difficulty_badge}</div>
                    </div>
                    <div class="meta-card">
                        <div class="meta-label">🏷️ Tags</div>
                        <div class="meta-value" style="padding-top: 4px;">{tag_badges}</div>
                    </div>
                </div>
                
                <h3 style="font-size: 22px; font-weight: 600; color: #1F2937; margin-bottom: 12px; border-bottom: 2px solid #F1F5F9; padding-bottom: 6px;">🛒 Ingredients</h3>
                {chips_html}
                
                <h3 style="font-size: 22px; font-weight: 600; color: #1F2937; margin-top: 24px; margin-bottom: 12px; border-bottom: 2px solid #F1F5F9; padding-bottom: 6px;">🍳 Instructions</h3>
                {steps_html}
                
                <div class="chef-tip-box">
                    <div class="chef-tip-title">💡 Chef's Tip</div>
                    <div class="chef-tip-content">{recipe['note']}</div>
                </div>
            </div>
        </div>
        """
        st.markdown(clean_html(recipe_html), unsafe_allow_html=True)
    else:
        placeholder_html = """
        <div class="welcome-placeholder">
            <div class="welcome-icon">🍳</div>
            <div class="welcome-title">Ready to Cook?</div>
            <p style="font-size: 15px; max-width: 380px; margin: 0 auto; line-height: 1.5;">Enter or upload your ingredients on the left panel, and click "Generate Recipe" to view your custom recipe card.</p>
        </div>
        """
        st.markdown(clean_html(placeholder_html), unsafe_allow_html=True)

