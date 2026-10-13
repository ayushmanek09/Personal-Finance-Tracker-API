
import pytest
import run
from app import database

app = run.app


@pytest.fixture
def client(tmp_path, monkeypatch):
    test_db = tmp_path / "test_finance.db"
    monkeypatch.setattr(database, "DATABASE", str(test_db))
    database.init_db()

    app.config["TESTING"] = True

    with app.test_client() as test_client:
        yield test_client


def sample_transaction():
    return {
        "title": "Groceries",
        "amount": 500,
        "category": "Food",
        "transaction_type": "expense",
        "date": "2026-10-13",
    }


def test_create_transaction(client):
    response = client.post(
        "/transactions", json=sample_transaction()
    )

    assert response.status_code == 201
    assert response.json["message"] == "Transaction created"


def test_get_transactions(client):
    client.post("/transactions", json=sample_transaction())

    response = client.get("/transactions")

    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["title"] == "Groceries"


def test_update_transaction(client):
    created = client.post(
        "/transactions", json=sample_transaction()
    )
    transaction_id = created.json["id"]

    updated = sample_transaction()
    updated["title"] = "Weekly Groceries"
    updated["amount"] = 600

    response = client.put(
        f"/transactions/{transaction_id}", json=updated
    )

    assert response.status_code == 200
    assert response.json["message"] == "Transaction updated"


def test_delete_transaction(client):
    created = client.post(
        "/transactions", json=sample_transaction()
    )
    transaction_id = created.json["id"]

    response = client.delete(f"/transactions/{transaction_id}")

    assert response.status_code == 200
    assert response.json["message"] == "Transaction deleted"


def test_reject_negative_amount(client):
    data = sample_transaction()
    data["amount"] = -10

    response = client.post("/transactions", json=data)

    assert response.status_code == 400
    assert response.json["error"] == "Amount must be positive"


def test_summary(client):
    income = sample_transaction()
    income.update({
        "title": "Salary",
        "amount": 2000,
        "category": "Work",
        "transaction_type": "income",
    })

    expense = sample_transaction()
    expense["amount"] = 500

    client.post("/transactions", json=income)
    client.post("/transactions", json=expense)

    response = client.get("/summary")

    assert response.status_code == 200
    assert response.json["total_income"] == 2000
    assert response.json["total_expenses"] == 500
    assert response.json["balance"] == 1500


def test_missing_transaction_returns_404(client):
    response = client.get("/transactions/999")

    assert response.status_code == 404
    assert response.json["error"] == "Transaction not found"


def test_filter_by_transaction_type(client):
    expense = sample_transaction()
    client.post("/transactions", json=expense)

    income = sample_transaction()
    income["transaction_type"] = "income"
    income["title"] = "Salary"
    client.post("/transactions", json=income)

    response = client.get("/transactions?transaction_type=expense")

    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["transaction_type"] == "expense"


def test_invalid_transaction_type_filter(client):
    response = client.get("/transactions?transaction_type=invalid")

    assert response.status_code == 400
    assert response.json["error"] == "Invalid transaction type"
