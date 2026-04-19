from flask import Flask, render_template, request, jsonify
from pipeline import run_research_pipeline
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    topic = data.get("topic")

    result = run_research_pipeline(topic)

    return jsonify({
        "report": result["report"],
        "feedback": result["feedback"]
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
