import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel(model="gemini-2.5-flash")


def load_prompt():
    """
    Loads the prompt from the prompt.txt file.

    Returns:
        str: The content of the prompt file.
    """
    with open("prompt/prompt.txt", "r") as file:
        return file.read()

prompt = load_prompt()  # Load the prompt from the file
    
def generate_response(question,context):
    """
    Generates a response from the Google Gemini model based on the provided prompt.

    Args:
        prompt (str): The input prompt for the model.
    """
    # Combine the prompt, context, and question into a single input for the model
    combined_input = f"{prompt}\n\nContext: {context}\n\nQuestion: {question}"

    # Generate a response using the Google Gemini model
    response = model.generate_text(
        input=combined_input,
        temperature=0.7,
        max_output_tokens=200
    )

    return response.text  # Return the generated text from the model

