from flask import Flask, request, jsonify, send_from_directory, render_template_string
from flask_cors import CORS
import random
import os

app = Flask(__name__)
# CORS is essential to allow the browser to talk to the Flask server
CORS(app) 

# Get the exact directory where this app.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    """Serves the frontend. If missing, shows a helpful setup dashboard."""
    file_name = 'quiz_app.html'
    file_path = os.path.join(BASE_DIR, file_name)
    
    if not os.path.exists(file_path):
        files_in_dir = os.listdir(BASE_DIR)
        return render_template_string("""
            <body style="font-family:sans-serif; background:#f8fafc; padding:50px; line-height:1.6;">
                <div style="max-width:600px; margin:0 auto; background:white; padding:40px; border-radius:20px; box-shadow:0 10px 25px rgba(0,0,0,0.05); border:1px solid #e2e8f0;">
                    <h1 style="color:#ef4444; margin-top:0;">⚠️ File Not Found</h1>
                    <p>Flask is running, but it cannot find <b>{{ name }}</b>.</p>
                    <p><b>Expected Folder:</b><br><code style="background:#f1f5f9; padding:5px 10px; border-radius:5px; display:block; margin-top:10px;">{{ path }}</code></p>
                    <p><b>Files actually in this folder:</b> {{ files }}</p>
                    <div style="margin-top:20px; padding:15px; background:#eff6ff; border-radius:10px; color:#1e40af;">
                        <b>Fix:</b> Rename your HTML file to <code>quiz_app.html</code> and place it in the folder listed above.
                    </div>
                </div>
            </body>
        """, name=file_name, path=BASE_DIR, files=files_in_dir), 404
        
    response = send_from_directory(BASE_DIR, file_name)
    # Prevent browser from caching old broken versions
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return response

# Standard Knowledge Bank
QUESTION_BANK = {
    "AI": [
        {"q": "What is the primary goal of the Turing Test?", "o": ["Measure intelligence", "Test hardware speed", "Check connectivity", "Data encryption"], "a": 0},
        {"q": "Which algorithm is commonly used for classification?", "o": ["K-Means", "Random Forest", "A* Search", "Dijkstra"], "a": 1},
        {"q": "What does 'NLP' stand for?", "o": ["Natural Language Processing", "Node Logic", "Network Layer", "Next Level Physics"], "a": 0},
        {"q": "Who is considered the father of AI?", "o": ["Alan Turing", "John McCarthy", "Elon Musk", "Bill Gates"], "a": 1},
        {"q": "What is a Neural Network modeled after?", "o": ["Computer CPU", "Human Brain", "Social Network", "Electric Grid"], "a": 1}
    ],
    "PYTHON": [
        {"q": "What is the result of 3 * '3'?", "o": ["9", "333", "Error", "None"], "a": 1},
        {"q": "Which keyword is used for exception handling?", "o": ["catch", "except", "error", "handle"], "a": 1},
        {"q": "What is a 'List Comprehension'?", "o": ["Zip tool", "Concise list creation", "Debug tool", "Documentation style"], "a": 1},
        {"q": "Which of these is an immutable type?", "o": ["List", "Dictionary", "Set", "Tuple"], "a": 3},
        {"q": "# is used for what in Python?", "o": ["Division", "Comments", "Header", "List"], "a": 1}
    ],
    "JAVA": [
        {"q": "Which company developed Java?", "o": ["Microsoft", "Google", "Sun Microsystems", "Apple"], "a": 2},
        {"q": "What is the entry point method in Java?", "o": ["start()", "init()", "main()", "run()"], "a": 2},
        {"q": "Which keyword creates a subclass?", "o": ["implements", "extends", "inherits", "super"], "a": 1},
        {"q": "Is Java platform-independent?", "o": ["No", "Yes", "Only on Windows", "Only on Linux"], "a": 1},
        {"q": "What is the size of 'int'?", "o": ["16-bit", "32-bit", "64-bit", "8-bit"], "a": 1}
    ],
    "DBMS": [
        {"q": "Which SQL clause filters groups?", "o": ["WHERE", "HAVING", "ORDER BY", "GROUP BY"], "a": 1},
        {"q": "What does 'ACID' stand for?", "o": ["Atomicity, Consistency, Isolation, Durability", "Access, Control, Info, Data", "Always Correct", "Audit Check"], "a": 0},
        {"q": "A Primary Key must be...", "o": ["Unique but can be null", "Unique and not null", "Shared", "A string"], "a": 1},
        {"q": "Which command removes all records?", "o": ["DELETE", "REMOVE", "TRUNCATE", "DROP"], "a": 2},
        {"q": "Normalization is for...", "o": ["Speed", "Reducing redundancy", "Backup", "Formatting"], "a": 1}
    ],
    "GENERAL": [
        {"q": "Which is the smallest continent?", "o": ["Europe", "Australia", "Antarctica", "Africa"], "a": 1},
        {"q": "What is the symbol for Gold?", "o": ["Gd", "Ag", "Au", "Fe"], "a": 2},
        {"q": "How many bones in adult humans?", "o": ["206", "180", "215", "300"], "a": 0},
        {"q": "Which is the Red Planet?", "o": ["Venus", "Mars", "Jupiter", "Saturn"], "a": 1},
        {"q": "Who wrote Romeo and Juliet?", "o": ["Dickens", "Shakespeare", "Twain", "Austen"], "a": 1}
    ]
}

@app.route('/generate-quiz', methods=['POST'])
def generate_quiz():
    try:
        data = request.json
        topic = data.get('topic', 'GENERAL').upper()
        count = int(data.get('count', 5))
        
        # Topic matching logic
        template = QUESTION_BANK.get(topic)
        if not template:
            for key in QUESTION_BANK.keys():
                if key in topic:
                    template = QUESTION_BANK[key]
                    break
            if not template:
                template = QUESTION_BANK["GENERAL"]
        
        selected = random.sample(template, min(len(template), count))
        
        # Ensure we meet the count requirement by cycling if necessary
        final_questions = []
        for i in range(count):
            base = selected[i % len(selected)]
            final_questions.append({
                "id": i,
                "question": base['q'],
                "options": base['o'],
                "correct": base['a']
            })

        return jsonify({"status": "success", "questions": final_questions, "topic": topic})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    print(f"\n--- AI Quiz Master Backend ---")
    print(f"Working Directory: {BASE_DIR}")
    print(f"Server starting at: http://127.0.0.1:5000\n")
    app.run(port=5000, debug=True)