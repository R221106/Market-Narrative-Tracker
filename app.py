from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Hello World"

@app.route("/data")
def data():
    return jsonify({
        "name":"AI"
    })

if __name__ == "__main__":
    app.run(debug=True)
