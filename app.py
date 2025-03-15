from flask import Flask, render_template, request, jsonify
from chat import get_response
from rapidfuzz import process

app = Flask(__name__)

# List of common words in chatbot responses
patterns = ["Hello", "Internship", "Requirements", "Application", "Stipend", "internship_duration", "Process","interview_process", "Goodbye"]

def correct_spelling(user_input):
    """Corrects spelling mistakes in user input using RapidFuzz"""
    best_match = process.extractOne(user_input, patterns)
    if best_match and best_match[1] > 80:  # 80% similarity threshold
        return best_match[0]  # Return corrected word
    return user_input  # Return original if no good match

@app.route("/")
def index_get():
    return render_template("base.html", script_root=request.script_root or "")

@app.post("/predict")
def predict():
    text = request.get_json().get("message")  

    if not text:
        return jsonify({"answer": "I didn't receive a message. Please try again."})

    corrected_text = correct_spelling(text)  # Correct spelling before processing
    response = get_response(corrected_text)  # Get chatbot response
    message = {"answer": response}
    
    return jsonify(message)

if __name__ == "__main__":
    app.run(debug=True)
