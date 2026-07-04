from pydantic import BaseModel, Field

class Substitution(BaseModel):
    """
    Represents an ingredient substitution recommendation.
    """
    ingredient: str = Field(..., description="The original ingredient to replace.")
    substitute: str = Field(..., description="The suggested replacement ingredient.")

class MealPlan(BaseModel):
    """
    Represents a full single-day meal plan recommendation.
    """
    breakfast: str = Field(..., description="Breakfast meal description.")
    lunch: str = Field(..., description="Lunch meal description.")
    dinner: str = Field(..., description="Dinner meal description.")
    grocery_list: list[str] = Field(..., description="List of grocery items required for the meal plan.")
    substitutions: list[Substitution] = Field(..., description="List of smart ingredient substitutions.")
    budget_feasibility: str = Field(..., description="Summary explanation of whether the meal plan fits the budget.")
