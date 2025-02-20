from flask import Flask, request, jsonify, render_template
import pandas as pd
import google.generativeai as genai
import os

app = Flask(__name__)

# Load crane data from local CSV file (Change this to your actual file path)
LOCAL_CSV_PATH = "C:\\Users\\Yogesh V\\Downloads\\Cranes_models_updated (1).csv"  # Update this path
crane_df = pd.read_csv(LOCAL_CSV_PATH)

# Set up Gemini API (Replace with your API key)
GEMINI_API_KEY = "AIzaSyAQOKTy2c7e2vglCvF1zpDv9lUYgvdTn2w"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chatbot", methods=["POST"])
def chatbot():
    user_input = request.json.get("query").strip().lower()

    # Check for crane specifications in CSV
    for column in crane_df.columns:
        if user_input in column.lower():
            value = crane_df[column].mode()[0]  # Get the most common value
            return jsonify({"response": f"{column}: {value}"})

    # If not found, use Gemini AI (Shortened Response)
    gemini_response = model.generate_content(user_input)
    short_response = " ".join(gemini_response.text.split(".")[:2])  # First 1-2 sentences
    return jsonify({"response": short_response})

if __name__ == "__main__":
    app.run(debug=True)