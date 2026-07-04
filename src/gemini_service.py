import os
import json
from google import genai
from google.genai.errors import APIError
from src.models import MealPlan

class GeminiService:
    """
    Service class to handle all interactions with the Google Gemini API.
    """
    def __init__(self):
        """
        Initializes the Gemini client. Verifies that the GEMINI_API_KEY is available.
        """
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY is missing. Please set it in your environment or .env file."
            )
        
        # Initialize Client. Under the hood, it uses GEMINI_API_KEY from environment variables.
        self.client = genai.Client()

    def generate_meal_plan(self, day_description: str, budget: str) -> dict:
        """
        Generates a structured, budget-checked meal plan based on the user's day and budget target.

        Args:
            day_description (str): How the user's day is looking.
            budget (str): The target food budget constraint.

        Returns:
            dict: A dictionary containing breakfast, lunch, dinner, grocery_list, substitutions, 
                  and budget_feasibility.

        Raises:
            APIError: If the Gemini API returns an error.
            json.JSONDecodeError: If the response text cannot be parsed as JSON.
        """
        prompt = f"""
        Generate a 1-day meal plan based on this user's day: "{day_description}"
        Target Budget constraint: "{budget}"
        
        Provide:
        1. Simple Breakfast, Lunch, and Dinner ideas that fit their energy levels.
        2. A consolidated grocery list.
        3. Smart substitutions for main ingredients.
        4. A quick budget feasibility check explaining if it fits their target.
        """
        
        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config={
                    'response_mime_type': 'application/json',
                    'response_schema': MealPlan,
                }
            )
            
            if not response.text:
                raise APIError(None, None, "The model returned an empty response.")
                
            return json.loads(response.text)
        except Exception as e:
            # Propagate exception to be handled gracefully by UI layer
            raise e
