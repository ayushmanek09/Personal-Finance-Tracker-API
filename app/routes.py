
from flask import Blueprint, request, jsonify
from app.database import get_db_connection

transactions_bp = Blueprint("transactions", __name__)


@transactions_bp.route("/transactions", methods=["POST"])
def create_transaction():
    data = request.get_json(silent=True) or {}

    required = ["title", "amount", "category", "transaction_type", "date"]
    if any(field not in data for field in required):
        return jsonify({"error": "All fields are required"}), 400

    try:
        amount = float(data["amount"])
    except (ValueError, TypeError):
        return jsonify({"error": "Amount must be a number"}), 400

    if amount <= 0:
        return jsonify({"error": "Amount must be positive"}), 400

    if data["transaction_type"] not in ["income", "expense"]:
        return jsonify({"error": "Type must be income or expense"}), 400

    connection = get_db_connection()
    cursor = connection.execute(
        """INSERT INTO transactions
        (title, amount, category, transaction_type, date)
        VALUES (?, ?, ?, ?, ?)""",
        (
            data["title"],
            amount,
            data["category"],
            data["transaction_type"],
            data["date"],
        ),
    )
    connection.commit()
    transaction_id = cursor.lastrowid
    connection.close()

    return jsonify({
        "message": "Transaction created",
        "id": transaction_id,
    }), 201



@transactions_bp.route("/transactions", methods=["GET"])
def get_transactions():
    query = "SELECT * FROM transactions WHERE 1=1"
    params = []

    category = request.args.get("category")
    transaction_type = request.args.get("transaction_type")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    if category:
        query += " AND category = ?"
        params.append(category)

    if transaction_type:
        if transaction_type not in ["income", "expense"]:
            return jsonify({"error": "Invalid transaction type"}), 400
        query += " AND transaction_type = ?"
        params.append(transaction_type)

    if start_date:
        query += " AND date >= ?"
        params.append(start_date)

    if end_date:
        query += " AND date <= ?"
        params.append(end_date)

    query += " ORDER BY date DESC, id DESC"

    connection = get_db_connection()
    rows = connection.execute(query, params).fetchall()
    connection.close()

    return jsonify([dict(row) for row in rows]), 200



@transactions_bp.route("/transactions/<int:transaction_id>", methods=["GET"])
def get_transaction(transaction_id):
    connection = get_db_connection()
    row = connection.execute(
        "SELECT * FROM transactions WHERE id = ?",
        (transaction_id,),
    ).fetchone()
    connection.close()

    if row is None:
        return jsonify({"error": "Transaction not found"}), 404

    return jsonify(dict(row)), 200


@transactions_bp.route("/transactions/<int:transaction_id>", methods=["PUT"])
def update_transaction(transaction_id):
    data = request.get_json(silent=True) or {}
    required = ["title", "amount", "category", "transaction_type", "date"]

    if any(field not in data for field in required):
        return jsonify({"error": "All fields are required"}), 400

    try:
        amount = float(data["amount"])
    except (ValueError, TypeError):
        return jsonify({"error": "Amount must be a number"}), 400

    if amount <= 0:
        return jsonify({"error": "Amount must be positive"}), 400

    if data["transaction_type"] not in ["income", "expense"]:
        return jsonify({"error": "Type must be income or expense"}), 400

    connection = get_db_connection()
    existing = connection.execute(
        "SELECT id FROM transactions WHERE id = ?",
        (transaction_id,),
    ).fetchone()

    if existing is None:
        connection.close()
        return jsonify({"error": "Transaction not found"}), 404

    connection.execute(
        """UPDATE transactions
        SET title = ?, amount = ?, category = ?,
            transaction_type = ?, date = ?
        WHERE id = ?""",
        (
            data["title"],
            amount,
            data["category"],
            data["transaction_type"],
            data["date"],
            transaction_id,
        ),
    )
    connection.commit()
    connection.close()

    return jsonify({"message": "Transaction updated"}), 200


@transactions_bp.route("/transactions/<int:transaction_id>", methods=["DELETE"])
def delete_transaction(transaction_id):
    connection = get_db_connection()
    cursor = connection.execute(
        "DELETE FROM transactions WHERE id = ?",
        (transaction_id,),
    )
    connection.commit()
    connection.close()

    if cursor.rowcount == 0:
        return jsonify({"error": "Transaction not found"}), 404

    return jsonify({"message": "Transaction deleted"}), 200


@transactions_bp.route("/summary", methods=["GET"])
def get_summary():
    connection = get_db_connection()

    row = connection.execute("""
        SELECT
            COALESCE(SUM(CASE WHEN transaction_type = 'income'
                THEN amount ELSE 0 END), 0) AS total_income,
            COALESCE(SUM(CASE WHEN transaction_type = 'expense'
                THEN amount ELSE 0 END), 0) AS total_expenses
        FROM transactions
    """).fetchone()

    connection.close()

    income = row["total_income"]
    expenses = row["total_expenses"]

    return jsonify({
        "total_income": income,
        "total_expenses": expenses,
        "balance": income - expenses,
    }), 200
