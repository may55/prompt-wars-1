import streamlit as st
from dotenv import load_dotenv
from src.gemini_service import GeminiService
from src.ui_components import (
    inject_custom_css,
    render_header,
    render_meal_card,
    render_substitutions_section,
    render_budget_feasibility
)

# Load environment variables from .env file
load_dotenv()

# Initialize Streamlit page config
st.set_page_config(
    page_title="AI cooking todo list",
    page_icon="🍳",
)

# Inject modern Custom CSS
inject_custom_css()

# Render Title Header
render_header()

# Initialize session state for the meal plan to persist across interactions
if "meal_plan" not in st.session_state:
    st.session_state["meal_plan"] = None

# Input Fields
day_description = st.text_area("How is your day looking? (e.g., 'Busy workday, tired, need comfort food')")
budget = st.text_input("What is your target budget for today's food? (e.g., '$15 total', 'Using pantry staples')")

# Generate Button Action
if st.button("Generate Plan", type="primary"):
    if not day_description:
        st.error("Please describe your day first!")
    else:
        try:
            # Initialize the modular service
            service = GeminiService()
            
            with st.spinner("Analyzing your day and calculating budgets..."):
                # Call Gemini for a structured meal plan
                data = service.generate_meal_plan(day_description, budget)
                # Store in session state to persist when user checks grocery list items
                st.session_state["meal_plan"] = data
                st.success("Plan Generated!")
        except ValueError as ve:
            st.error(str(ve))
        except Exception as e:
            st.error(f"An error occurred while generating your plan: {str(e)}")

# Display the Meal Plan if it is available in the session state
if st.session_state["meal_plan"] is not None:
    data = st.session_state["meal_plan"]
    
    # 1. Menu Section
    st.markdown(
        "<h2 style='margin-top: 1.5rem; text-align: center; color: #1A2B4C;'>🍽️ Your Daily Menu</h2>", 
        unsafe_allow_html=True
    )
    col1, col2, col3 = st.columns(3)
    with col1:
        render_meal_card("🍳 Breakfast", data.get('breakfast', ''), "#3A86FF")
    with col2:
        render_meal_card("🥗 Lunch", data.get('lunch', ''), "#4D96FF")
    with col3:
        render_meal_card("🍲 Dinner", data.get('dinner', ''), "#4CC9F0")
        
    st.markdown("<hr style='border: 0; border-top: 1px solid #E2E8F0; margin: 2rem 0;' />", unsafe_allow_html=True)
    
    # 2. Grocery List Section
    st.markdown("<h2 style='color: #2C3E50;'>🛒 Interactive Grocery List</h2>", unsafe_allow_html=True)
    grocery_list = data.get('grocery_list', [])
    if grocery_list:
        for idx, item in enumerate(grocery_list):
            # Using unique keys (index + item hash) prevents duplicate key exceptions on rendering
            st.checkbox(item, key=f"grocery_{idx}_{hash(item)}")
    else:
        st.info("No grocery items required.")
        
    st.markdown("<hr style='border: 0; border-top: 1px solid #E2E8F0; margin: 2rem 0;' />", unsafe_allow_html=True)
    
    # 3. Substitutions Section
    render_substitutions_section(data.get('substitutions', []))
    
    st.markdown("<hr style='border: 0; border-top: 1px solid #E2E8F0; margin: 2rem 0;' />", unsafe_allow_html=True)
    
    # 4. Budget Feasibility Section
    render_budget_feasibility(data.get('budget_feasibility', ''))