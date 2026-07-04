import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

print("GEMINI_API_KEY starts with:", os.environ.get("GEMINI_API_KEY", "")[:10])

try:
    client = genai.Client()
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents='Hello'
    )
    print("Success! Response:", response.text)
except Exception as e:
    print("Failed with error:", type(e), str(e))
