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

def get_user_friendly_error(e: Exception) -> str:
    """
    Translates technical exceptions into polite, user-friendly messages.
    """
    if isinstance(e, ValueError):
        # User-friendly value error from validation
        return str(e)
        
    if isinstance(e, APIError):
        code = getattr(e, "code", None)
        message = getattr(e, "message", str(e))
        msg_lower = message.lower()
        
        if code == 400 or "api key not valid" in msg_lower or "api_key" in msg_lower:
            return "🔑 The Gemini API key configured is invalid or has expired. Please check your configuration."
        elif code == 403 or "permission denied" in msg_lower:
            return "🚫 Access denied. Your API key does not have permission to use the Gemini API."
        elif code == 429 or "quota exceeded" in msg_lower or "rate limit" in msg_lower:
            return "⏳ Rate limit exceeded or API quota exhausted. Please wait a moment before trying again."
        elif code == 503 or "service unavailable" in msg_lower:
            return "🛠️ The Gemini service is currently overloaded or undergoing maintenance. Please try again shortly."
        else:
            return "🤖 The AI service returned an error. Please verify your inputs and try again."
            
    # Check for network/connection errors
    err_str = str(e).lower()
    if "connect" in err_str or "timeout" in err_str or "dns" in err_str or "resolution" in err_str:
        return "🌐 Connection error. Please check your internet connection and try again."
        
    if "json" in err_str or "decode" in err_str:
        return "🧩 The AI returned an invalid response structure. Please try clicking 'Generate Plan' again."
        
    return "⚠️ An unexpected error occurred while generating your plan. Please check your inputs and try again."

