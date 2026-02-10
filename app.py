from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os, requests
from math import gcd
from functools import reduce
load_dotenv()

app = Flask(__name__)
CORS(app)

OFFICIAL_EMAIL = "kabir0787.be23@chitkara.edu.in"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

print(GEMINI_API_KEY)
def fibonacci(n):
    if n <= 0:
        return []
    res = [0, 1]
    for i in range(2, n):
        res.append(res[-1] + res[-2])
    return res[:n]


def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def lcm_array(arr):
    return reduce(lambda a, b: abs(a * b) // gcd(a, b), arr)


def hcf_array(arr):
    return reduce(gcd, arr)


def get_ai_answer(q):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key={GEMINI_API_KEY}"
    payload = {"contents": [{"parts": [{"text": f"give the answer in exactly one word, dont add punctuation, or dont add any explanation question:{q}"}]}]}
    r = requests.post(url, json=payload, timeout=10)
    r.raise_for_status()
    text = r.json()["candidates"][0]["content"]["parts"][0]["text"]
    return text.strip().split()[0]


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "is_success": True,
        "official_email": OFFICIAL_EMAIL
    }), 200


@app.route("/bfhl", methods=["POST"])
def bfhl():
    try:
        body = request.get_json()
        if not body or len(body) != 1:
            return jsonify({"is_success": False}), 400

        key = list(body.keys())[0]
        value = body[key]

        if key == "fibonacci":
            data = fibonacci(value)
        elif key == "prime":
            data = [x for x in value if is_prime(x)]
        elif key == "lcm":
            data = lcm_array(value)
        elif key == "hcf":
            data = hcf_array(value)
        elif key == "AI":
            data = get_ai_answer(value)
        else:
            return jsonify({"is_success": False}), 400

        return jsonify({
            "is_success": True,
            "official_email": OFFICIAL_EMAIL,
            "data": data
        }), 200

    except Exception:
        return jsonify({"is_success": False}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
