from flask import Flask, request, jsonify
from groq import Groq
from dotenv import load_dotenv
import os
import json
import streamlit as st
import requests
import threading
import time

load_dotenv()

app = Flask(__name__)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

BATCH_SIZE = 10

@app.route("/")
def home():
    return {"status": "Grouped Sentiment API running"}

def chunk(data, size):
    for i in range(0, len(data), size):
        yield data[i:i+size]

@app.route("/sentiment", methods=["POST"])
def sentiment():

    data = request.get_json(force=True)

    positive = []
    negative = []
    neutral = []

    for batch in chunk(data, BATCH_SIZE):

        prompt = f"""
You are a JSON API.

Return ONLY valid JSON array.
No explanation. No markdown.

Format:
[
  {{"id":1,"sentiment":"positive"}}
]

Sentiment must be ONLY:
positive, negative, neutral.

Input:
{json.dumps(batch)}
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role":"user","content":prompt}],
            temperature=0
        )

        raw = response.choices[0].message.content.strip()

        try:
            result = json.loads(raw)
        except:
            return jsonify({"error": "Invalid JSON from model", "raw": raw})

        for r in result:
            if r["sentiment"] == "positive":
                positive.append(r["id"])
            elif r["sentiment"] == "negative":
                negative.append(r["id"])
            else:
                neutral.append(r["id"])

    return jsonify({
        "positive": positive,
        "negative": negative,
        "neutral": neutral,
        "counts":{
            "positive": len(positive),
            "negative": len(negative),
            "neutral": len(neutral)
        }
    })

# ---------- Run Flask inside Streamlit ----------

def run_flask():
    app.run(port=5001, use_reloader=False)

if "flask_started" not in st.session_state:
    st.session_state.flask_started = True
    threading.Thread(target=run_flask, daemon=True).start()
    time.sleep(2)

# ---------- Streamlit UI ----------

st.title("Sentiment Classifier (Groq + Flask + Streamlit)")

default = """[
 {"id":1,"text":"I love this product"},
 {"id":2,"text":"Worst experience"},
 {"id":3,"text":"It is okay"}
]"""

uploaded = st.file_uploader("Upload JSON file", type=["json"])

if uploaded:
    payload = json.load(uploaded)
else:
    text = st.text_area("Or paste JSON here:", default, height=200)
    payload = json.loads(text)

if st.button("Analyze"):

    try:
        res = requests.post(
            "http://127.0.0.1:5001/sentiment",
            json=payload
        )

        st.subheader("Grouped Result")
        st.json(res.json())

    except Exception as e:
        st.error(str(e))

