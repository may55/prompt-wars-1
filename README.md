# 🍳 AI Meal Planner

A sleek, modern, and budget-conscious meal planning application. Built with **Streamlit** and powered by **Google Gemini 2.5 Flash**, it converts user-described days (e.g., energy levels, schedule, mood) and target budgets into personalized, structured meal plans instantly.

---

## ⚡ Key Features

- **Personalized Daily Menu**: Tailors Breakfast, Lunch, and Dinner suggestions specifically to your day's schedule and energy.
- **Interactive Grocery List**: A checkable shopping checklist that persists interactive states across reruns (using Streamlit `session_state`).
- **Smart Substitutions**: Ingredient replacements highlighting options to avoid and suggestible alternatives.
- **Budget Feasibility Check**: Checks and explains whether the suggested meals comfortably fit within your specified target budget.
- **HTML Sanitization**: Inputs and outputs are programmatically escaped to prevent HTML injection/XSS vulnerabilities.
- **Premium Styling**: Polished light-mode layout using modern typography and card containers with hover effects.

---

## 📂 Project Architecture

The project follows a clean, modular architecture:

```text
├── app.py                   # Main entrypoint; coordinates UI and session state
├── requirements.txt         # Package dependencies with pinned versions
├── .gitignore               # Ignored environments (e.g., .env)
└── src/
    ├── __init__.py          # Module initialization
    ├── models.py            # Pydantic schemas enforcing Gemini structured output
    ├── gemini_service.py    # Service wrapper for Google Gemini client API
    └── ui_components.py     # Custom CSS styles, HTML cards, and escaping helpers
```

---

## 🛠️ Local Setup

### 1. Prerequisites
- Python 3.9 or higher.
- A Gemini API Key from Google AI Studio.

### 2. Clone and Install
Clone this repository and install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Configure Environments
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_actual_gemini_api_key
```

### 4. Run the App
Launch the Streamlit development server:
```bash
python3 -m streamlit run app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🚀 Deploying to Render

This project is ready to be hosted as a **Web Service** on Render:

1. **Connect Repository**: Link this GitHub repository to Render.
2. **Environment settings**:
   - **Language**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
3. **Environment Variables**: Add your key/value pairing under Advanced settings:
   - `GEMINI_API_KEY` = `[your_gemini_api_key]`
