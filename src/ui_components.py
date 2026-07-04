import html
import streamlit as st

def safe_html(val: str) -> str:
    """
    Escapes special characters in text to prevent HTML injection/XSS.
    
    Args:
        val (str): The raw text to escape.
        
    Returns:
        str: The escaped, HTML-safe string.
    """
    return html.escape(str(val))

def inject_custom_css():
    """
    Injects custom styles for the AI Meal Planner, ensuring high-quality,
    vibrant light mode UI.
    """
    st.markdown(
        """
        <style>
        /* Force Light Mode Background on everything */
        [data-testid="stAppViewContainer"], .stApp, html, body {
            background-color: #FFFFFF !important;
            background: linear-gradient(135deg, #F0F5FA 0%, #FFFFFF 100%) !important;
        }
        
        /* Make the header element transparent */
        [data-testid="stHeader"] {
            background-color: transparent !important;
        }
        
        /* Main container padding */
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
            max-width: 800px;
        }
        
        /* Target paragraph and list element styles inside markdown container specifically */
        div[data-testid="stMarkdownContainer"] p, .stMarkdown p, .stMarkdown li {
            color: #2C3E50 !important;
            font-size: 16px !important;
        }
        
        /* Input field label styles */
        .stWidgetLabel p {
            color: #1A2B4C !important;
            font-weight: 600 !important;
            font-size: 17px !important;
            margin-bottom: 8px !important;
        }
        
        /* Customize text areas and input fields */
        .stTextArea textarea {
            border-radius: 12px !important;
            border: 1px solid #D6E4F0 !important;
            background-color: #FFFFFF !important;
            color: #1A2B4C !important;
            font-size: 17px !important;
            padding: 12px !important;
            transition: all 0.2s ease-in-out !important;
        }
        .stTextInput input {
            border-radius: 12px !important;
            border: 1px solid #D6E4F0 !important;
            background-color: #FFFFFF !important;
            color: #1A2B4C !important;
            font-size: 17px !important;
            padding: 10px 14px !important;
            transition: all 0.2s ease-in-out !important;
        }
        .stTextArea textarea:focus, .stTextInput input:focus {
            border-color: #3A86FF !important;
            box-shadow: 0 0 0 3px rgba(58, 134, 255, 0.15) !important;
        }
        
        /* Style the Primary Button */
        div.stButton > button:first-child {
            background-color: #3A86FF !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 0.7rem 2rem !important;
            font-weight: 600 !important;
            font-size: 18px !important;
            width: 100% !important;
            box-shadow: 0 4px 10px rgba(58, 134, 255, 0.25) !important;
            transition: all 0.2s ease-in-out !important;
            cursor: pointer !important;
        }
        div.stButton > button:first-child:hover {
            background-color: #2563EB !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 6px 14px rgba(58, 134, 255, 0.35) !important;
        }
        div.stButton > button:first-child:active {
            transform: translateY(1px) !important;
        }
        
        /* Headers & Text colors */
        h1, h2, h3, h4, h5 {
            color: #1A2B4C !important;
            font-family: 'Outfit', 'Inter', sans-serif !important;
        }
        
        /* Make check-boxes look clean and premium */
        .stCheckbox > label {
            background-color: #FFFFFF !important;
            color: #2C3E50 !important;
            padding: 14px 18px !important;
            border-radius: 10px !important;
            border: 1px solid #E2E8F0 !important;
            margin-bottom: 8px !important;
            width: 100% !important;
            display: flex !important;
            align-items: center !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important;
            transition: all 0.2s ease !important;
            font-size: 17px !important;
        }
        .stCheckbox > label:hover {
            border-color: #3A86FF !important;
            background-color: #F4F8FF !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def render_header():
    """
    Renders the custom styled main header for the application.
    """
    st.markdown(
        """
        <div style="text-align: center; width: 100%; margin: 1rem auto 2rem auto; padding: 0 10px;">
            <h1 style="color: #3A86FF; font-size: 2.4rem; font-weight: 800; margin: 0; line-height: 1.2; text-align: center; font-family: 'Outfit', 'Inter', sans-serif;">⚡ AI Meal Planner</h1>
            <p style="color: #4A5568; font-size: 18px; margin-top: 10px; margin-bottom: 0; text-align: center; font-family: 'Inter', sans-serif;">Tell the AI about your day, and get a structured, budget-checked plan instantly.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_meal_card(meal_type: str, meal_desc: str, border_color: str):
    """
    Renders a premium daily menu card for a meal category (Breakfast, Lunch, Dinner).
    
    Args:
        meal_type (str): The label of the meal, e.g. "🍳 Breakfast".
        meal_desc (str): Description of the meal.
        border_color (str): Border color code for styling.
    """
    escaped_desc = safe_html(meal_desc)
    st.markdown(
        f"""
        <div style="
            background-color: #FFFFFF; 
            padding: 22px; 
            border-radius: 14px; 
            box-shadow: 0 4px 10px rgba(0,0,0,0.04); 
            border-top: 6px solid {border_color};
            margin-bottom: 20px;
            min-height: 180px;
        ">
            <h4 style="margin: 0 0 10px 0; color: {border_color}; display: flex; align-items: center; gap: 8px; font-size: 19px;">{meal_type}</h4>
            <p style="color: #4A5568; font-size: 17px; line-height: 1.6; margin: 0;">{escaped_desc}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_substitutions_section(substitutions: list[dict]):
    """
    Renders the list of ingredient substitutions in structured cards.
    
    Args:
        substitutions (list[dict]): List of substitution items with keys 'ingredient' and 'substitute'.
    """
    st.markdown("<h2 style='color: #2C3E50; margin-bottom: 1.2rem;'>🔄 Smart Substitutions</h2>", unsafe_allow_html=True)
    
    if not substitutions:
        st.info("No substitutions needed for this menu.")
        return
        
    sub_html = "<div style='display: flex; flex-direction: column; gap: 12px; margin-bottom: 1.5rem;'>"
    for item in substitutions:
        orig = safe_html(item.get('ingredient', ''))
        sub = safe_html(item.get('substitute', ''))
        sub_html += f"""
        <div style="
            background-color: #FFFFFF; 
            padding: 16px; 
            border-radius: 12px; 
            box-shadow: 0 2px 6px rgba(0,0,0,0.02); 
            border: 1px solid #EAEAEA;
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            align-items: center;
            gap: 10px;
        ">
            <span style="font-weight: 600; color: #E53E3E; font-size: 17px;">❌ Instead of: {orig}</span>
            <span style="font-weight: 600; color: #38A169; font-size: 17px;">✅ Use: {sub}</span>
        </div>
        """
    sub_html += "</div>"
    st.markdown(sub_html, unsafe_allow_html=True)

def render_budget_feasibility(budget_feasibility: str):
    """
    Renders the budget feasibility section.
    
    Args:
        budget_feasibility (str): Explanation of whether the meal plan fits the budget.
    """
    st.markdown("<h2 style='color: #2C3E50;'>💰 Budget Feasibility Check</h2>", unsafe_allow_html=True)
    escaped_feasibility = safe_html(budget_feasibility)
    st.markdown(
        f"""
        <div style="
            background-color: #FFFAF0; 
            padding: 22px; 
            border-radius: 14px; 
            border-left: 6px solid #ED8936;
            box-shadow: 0 4px 8px rgba(237, 137, 54, 0.05);
        ">
            <p style="color: #DD6B20; font-weight: 700; font-size: 18px; margin: 0 0 6px 0;">Budget Feasibility Summary</p>
            <p style="color: #7B341E; font-size: 17px; line-height: 1.6; margin: 0;">{escaped_feasibility}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
