
# Personal Finance Tracker API

A RESTful API built with Python, Flask, and SQLite to manage personal income and expenses. Supports transaction CRUD operations, filtering, financial summaries, and automated tests.

## Features

- Create, retrieve, update, and delete transactions
- Filter transactions by category, type, and date range
- Calculate total income, total expenses, and balance
- Validate transaction amounts and types
- Store data using SQLite
- Automated tests using pytest

## Tech Stack

- Python
- Flask
- SQLite
- REST API
- pytest
- Git and GitHub

## Project Structure

    Personal-Finance-Tracker-API/
    ├── app/
    │   ├── __init__.py
    │   ├── database.py
    │   └── routes.py
    ├── tests/
    │   └── test_api.py
    ├── run.py
    ├── finance.db
    └── README.md

## Setup

### 1. Clone the repository

    git clone YOUR_REPOSITORY_URL
    cd Personal-Finance-Tracker-API

### 2. Create and activate a virtual environment

    python -m venv .venv
    source .venv/bin/activate

### 3. Install dependencies

    python -m pip install flask pytest

### 4. Start the API

    python run.py

The API will run at http://127.0.0.1:5000.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | / | API health check |
| POST | /transactions | Create a transaction |
| GET | /transactions | List transactions |
| GET | /transactions/<id> | Get one transaction |
| PUT | /transactions/<id> | Update a transaction |
| DELETE | /transactions/<id> | Delete a transaction |
| GET | /summary | Get financial summary |

### Filtering

Filter by category:

    GET /transactions?category=Food

Filter by transaction type:

    GET /transactions?transaction_type=expense

Filter by date range:

    GET /transactions?start_date=2026-10-01&end_date=2026-10-31

## Example Request

Create a transaction using curl:

    curl -X POST http://127.0.0.1:5000/transactions \
      -H "Content-Type: application/json" \
      -d '{"title":"Groceries","amount":500,"category":"Food","transaction_type":"expense","date":"2026-10-13"}'

## Run Tests

    python -m pytest -q

## Learning Outcomes

This project demonstrates REST API development, SQL database operations, input validation, HTTP status codes, query parameter filtering, and automated testing.

## Future Improvements

- Add user authentication
- Add pagination
- Improve monetary precision using integer minor units
- Add API documentation
- Deploy to AWS
