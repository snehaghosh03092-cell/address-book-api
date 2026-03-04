# Address Book API

A minimal RESTful API built with **FastAPI** to manage addresses.  
Users can create, update, delete, and search addresses within a given distance from a location.  
Data is stored in **SQLite** via **SQLAlchemy ORM**, and validation is handled using **Pydantic**.  

---

## Features

- Create, read, update, and delete addresses.
- Store addresses with **latitude** and **longitude**.
- Search addresses within a given distance from coordinates.
- Proper input validation and error handling.
- Logging for all incoming requests and database operations.
- Clean project structure with separate models, schemas, and CRUD logic.

---

## Quick Setup

```bash
# Clone the repository
git clone <your-repo-link>
cd address-book-api

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate   # Linux / Mac
# venv\Scripts\activate    # Windows

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if not exists
echo "DATABASE_URL=sqlite:///./addresses.db" >> .env
echo "DEBUG=True" >> .env

# Start FastAPI server
uvicorn app.main:app --reload

# Open Swagger UI
# http://127.0.0.1:8000/docs

## API Endpoints

- **POST** `/addresses/` → Create address
- **GET** `/addresses/{id}` → Get address by ID
- **PUT** `/addresses/{id}` → Update address
- **DELETE** `/addresses/{id}` → Delete address
- **GET** `/addresses/search` → Search addresses within distance

Sample JSON

1. Create / Update Address
   {
    "name": "Home",
    "street": "123 Main Street",
    "city": "Bengaluru",
    "latitude": 12.9716,
    "longitude": 77.5946
   }

2. Search Addresses
   GET /addresses/search?latitude=12.9716&longitude=77.5946&distance_km=5

PROJECT STRUCTURE

address-book-api/
├── app/
│   ├── main.py               # FastAPI app instance
│   ├── database.py           # SQLAlchemy engine & session
│   ├── config.py             # Environment settings
│   ├── logging_config.py     # Logger setup
│   ├── models/               # SQLAlchemy models
│   ├── schemas/              # Pydantic schemas
│   └── crud/                 # Database operations
├── .env                      # Environment variables
├── requirements.txt          # Python dependencies
├── .gitignore                # Ignore files
└── README.md                 # Project documentation

Logging

All requests, responses, and database errors are logged using Python’s logging module.
Example log output:

2026-03-04 14:44:34,935 [INFO Incoming request: POST http://127.0.0.1:8000/addresses/]
2026-03-04 14:44:34,936 [INFO Address 1 created successfully]
