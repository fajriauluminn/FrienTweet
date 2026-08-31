from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from db import init_db
import sqlite3
from model_loader import predict_text

app = Flask(__name__)
CORS(app)

init_db()

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/tweet")
def tweet():
    return render_template("tweet.html")


@app.route("/analysis")
def analysis():
    return render_template("analysis.html")


@app.route("/method")
def method():
    return render_template("method.html")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/predict", methods=["POST"])
def predict():

    try:
        data = request.json
        text = data["text"]

        result = predict_text(text)

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

@app.route("/tweet", methods=["POST"])
def save_tweet():
    data = request.json

    conn = sqlite3.connect("tweets.db", check_same_thread=False)
    c = conn.cursor()

    c.execute("""
        INSERT INTO tweets (username, text, date)
        VALUES (?, ?, ?)
    """, (data["username"], data["text"], data["date"]))

    conn.commit()
    conn.close()

    return jsonify({"status": "saved"})

@app.route("/tweets", methods=["GET"])
def get_tweets():
    conn = sqlite3.connect("tweets.db", check_same_thread=False)
    c = conn.cursor()

    c.execute("SELECT username, text, date FROM tweets ORDER BY id DESC")
    rows = c.fetchall()

    conn.close()

    tweets = []
    for r in rows:
        tweets.append({
            "username": r[0],
            "text": r[1],
            "date": r[2]
        })

    return jsonify(tweets)

if __name__ == "__main__":
    app.run(debug=True)