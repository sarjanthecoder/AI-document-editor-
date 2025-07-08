from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

GEMINI_API_KEY  = "AIzaSyDGgu2atNoJNEl8N92mFE7JqJcApk4vb84"
GEMINI_API_URL  = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-1.5-flash:generateContent"
    f"?key={GEMINI_API_KEY}"
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/generate", methods=["POST"])
def generate():
    prompt = (request.get_json() or {}).get("prompt", "").strip()
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        r = requests.post(GEMINI_API_URL, json=payload, timeout=15)
        r.raise_for_status()
        data = r.json()
        generated = (
            data.get("candidates", [{}])[0]
                .get("content", {})
                .get("parts", [{}])[0]
                .get("text", "")
        )
        return jsonify({"text": generated})
    except Exception as e:
        return jsonify({"error": str(e)}), 502

if __name__ == "__main__":
    app.run(debug=True)
