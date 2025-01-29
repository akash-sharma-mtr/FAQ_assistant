import json
from flask import Flask, request, render_template, jsonify
from modules.llm_integration import get_llm_response
from database.db_utils import get_connection
from database.db_utils import fetch_knowledge_base, log_interaction

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_query = request.json.get("query", "")
    knowledge_base = fetch_knowledge_base()

    # Look for a direct match in the knowledge base
    for entry in knowledge_base:
        if entry['question'].lower() in user_query.lower():
            answer = entry['answer']
            log_interaction(user_query, answer)
            return jsonify({"response": answer})

    # Use LLM for other queries
    response = get_llm_response(user_query)
    if not response:
        response = "I'm sorry, I couldn't find an answer to that. Can I help with something else?"
    log_interaction(user_query, response)
    return jsonify({"response": response})


@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        question = request.form.get("question")
        answer = request.form.get("answer")
        if question and answer:
            # Add new FAQ to the knowledge base (insert into DB)
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO knowledge_base (question, answer) VALUES (%s, %s)", (question, answer))
            connection.commit()
            connection.close()
    
    # Fetch knowledge base and logs to display
    knowledge_base = fetch_knowledge_base()
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM logs ORDER BY timestamp DESC LIMIT 10")
    logs = cursor.fetchall()
    connection.close()

    return render_template("admin.html", knowledge_base=knowledge_base, logs=logs)


@app.route("/update_kb", methods=["POST"])
def update_kb():
    file = request.files.get("file")
    if file:
        # Process the file (JSON, for example)
        knowledge_data = json.load(file)
        connection = get_connection()
        cursor = connection.cursor()
        for entry in knowledge_data:
            cursor.execute("INSERT INTO knowledge_base (question, answer) VALUES (%s, %s)", (entry['question'], entry['answer']))
        connection.commit()
        connection.close()
        return jsonify({"message": "Knowledge base updated successfully!"})
    return jsonify({"message": "No file uploaded!"})

if __name__ == "__main__":
    app.run(debug=True)
