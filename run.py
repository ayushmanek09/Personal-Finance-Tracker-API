
from flask import Flask, jsonify
from app.database import init_db
from app.routes import transactions_bp

app = Flask(__name__)

init_db()
app.register_blueprint(transactions_bp)


@app.route("/")
def home():
    return jsonify({
        "message": "Personal Finance Tracker API is running!"
    })


if __name__ == "__main__":
    app.run(debug=True)
