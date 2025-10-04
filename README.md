# 📊 Stadistics by Cuzzi

A FastAPI-based event tracking and analytics system for monitoring user interactions and generating real-time statistics.

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-green.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-red.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

---

## 🚀 Features

- **📝 Event Tracking**: Record user events with flexible JSON metadata
- **📊 Real-time Analytics**: Generate instant statistics from your data
- **🔍 Advanced Filtering**: Query events by user, type, date range, and more
- **⚡ High Performance**: Built with FastAPI for maximum speed
- **📈 Statistical Insights**:
  - Total event counts and unique users
  - Events breakdown by type
  - Most active users ranking
  - Time-series analysis (daily trends)
  - Per-user activity reports
  - Recent activity monitoring

---

## 📖 Table of Contents

- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [API Documentation](#-api-documentation)
- [Usage Examples](#-usage-examples)
- [Project Structure](#-project-structure)
- [Database Schema](#-database-schema)
- [Configuration](#-configuration)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

---

## ⚡ Quick Start

```bash
# Clone the repository
git clone https://github.com/Cuzzi-i/stadistics-by-cuzzi.git
cd stadistics-by-cuzzi

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn main:app --reload

# Open your browser
# API: http://localhost:8000
# Interactive Docs: http://localhost:8000/docs
```

---

## 🔧 Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Detailed Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Cuzzi-i/stadistics-by-cuzzi.git
   cd stadistics-by-cuzzi
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```
   The `--reload` flag enables hot-reloading during development.

5. **Verify installation**
   - Open http://localhost:8000 in your browser
   - You should see the API welcome message

---

## 📚 API Documentation

The API includes **automatic interactive documentation**:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Base URL
```
http://localhost:8000
```

---

## 🎯 API Endpoints

### 📝 Events Management

#### Create Event
**POST** `/events/`

Records a new event in the system.

**Request Body:**
```json
{
  "user_id": "user_123",
  "event_type": "page_view",
  "metadata": {
    "page": "/products",
    "duration": 45,
    "referrer": "google"
  }
}
```

**Response:**
```json
{
  "id": 1,
  "user_id": "user_123",
  "event_type": "page_view",
  "timestamp": "2025-10-04T12:30:00.123456",
  "metadata": {
    "page": "/products",
    "duration": 45,
    "referrer": "google"
  }
}
```

#### Get Events
**GET** `/events/`

Retrieve events with optional filters and pagination.

**Query Parameters:**
- `skip` (int): Number of records to skip (default: 0)
- `limit` (int): Maximum records to return (default: 100)
- `user_id` (string): Filter by user ID
- `event_type` (string): Filter by event type

**Example:**
```bash
GET /events/?user_id=user_123&limit=10
```

---

### 📊 Statistics Endpoints

#### Total Statistics
**GET** `/stats/total`

Get overall system statistics.

**Response:**
```json
{
  "total_events": 15420,
  "unique_users": 342,
  "unique_event_types": 12
}
```

#### Events by Type
**GET** `/stats/by-event-type`

Get event counts grouped by event type, sorted by frequency.

**Response:**
```json
[
  {
    "event_type": "page_view",
    "count": 8234
  },
  {
    "event_type": "click",
    "count": 4521
  },
  {
    "event_type": "purchase",
    "count": 2665
  }
]
```

#### Most Active Users
**GET** `/stats/by-user?limit=10`

Get the most active users ranked by event count.

**Query Parameters:**
- `limit` (int): Number of top users to return (default: 10)

**Response:**
```json
[
  {
    "user_id": "user_123",
    "count": 456
  },
  {
    "user_id": "user_456",
    "count": 387
  }
]
```

#### Events Over Time
**GET** `/stats/over-time?days=7`

Get daily event counts for a specified time period.

**Query Parameters:**
- `days` (int): Number of days to look back (default: 7)

**Response:**
```json
[
  {
    "date": "2025-10-01",
    "count": 1234
  },
  {
    "date": "2025-10-02",
    "count": 1567
  }
]
```

#### User Activity
**GET** `/stats/user-activity/{user_id}`

Get detailed statistics for a specific user.

**Response:**
```json
{
  "user_id": "user_123",
  "total_events": 456,
  "events_by_type": [
    {
      "event_type": "page_view",
      "count": 234
    },
    {
      "event_type": "click",
      "count": 222
    }
  ],
  "last_event_at": "2025-10-04T12:30:00.123456"
}
```

#### Recent Activity
**GET** `/stats/recent-activity?minutes=60`

Get activity within a recent time window.

**Query Parameters:**
- `minutes` (int): Time window in minutes (default: 60)

**Response:**
```json
{
  "time_window_minutes": 60,
  "total_events": 145,
  "by_type": [
    {
      "event_type": "page_view",
      "count": 89
    },
    {
      "event_type": "click",
      "count": 56
    }
  ]
}
```

---

## 💡 Usage Examples

### JavaScript / Node.js

```javascript
// Create an event
const createEvent = async () => {
  const response = await fetch('http://localhost:8000/events/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      user_id: 'user_123',
      event_type: 'button_click',
      metadata: {
        button: 'checkout',
        page: '/cart'
      }
    })
  });
  const data = await response.json();
  console.log('Event created:', data);
};

// Get statistics
const getStats = async () => {
  const response = await fetch('http://localhost:8000/stats/total');
  const stats = await response.json();
  console.log('Total stats:', stats);
};
```

### Python

```python
import requests

# Create an event
def create_event():
    response = requests.post(
        'http://localhost:8000/events/',
        json={
            'user_id': 'user_123',
            'event_type': 'purchase',
            'metadata': {
                'product_id': 'PROD-456',
                'amount': 99.99,
                'currency': 'USD'
            }
        }
    )
    print('Event created:', response.json())

# Get statistics
def get_statistics():
    response = requests.get('http://localhost:8000/stats/by-event-type')
    print('Events by type:', response.json())

# Get user activity
def get_user_activity(user_id):
    response = requests.get(f'http://localhost:8000/stats/user-activity/{user_id}')
    print('User activity:', response.json())
```

### cURL

```bash
# Create an event
curl -X POST "http://localhost:8000/events/" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123",
    "event_type": "login",
    "metadata": {
      "ip": "192.168.1.1",
      "device": "mobile",
      "browser": "Chrome"
    }
  }'

# Get total statistics
curl "http://localhost:8000/stats/total"

# Get events by type
curl "http://localhost:8000/stats/by-event-type"

# Get user's events
curl "http://localhost:8000/events/?user_id=user_123"

# Get recent activity (last hour)
curl "http://localhost:8000/stats/recent-activity?minutes=60"
```

---

## 🏗️ Project Structure

```
stadistics-by-cuzzi/
│
├── main.py              # FastAPI application and route handlers
├── models.py            # SQLAlchemy database models
├── schemas.py           # Pydantic validation schemas
├── database.py          # Database configuration and connection
│
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore rules
├── README.md           # This file
├── LICENSE             # MIT License
│
└── analytics.db        # SQLite database (auto-generated)
```

### File Descriptions

- **`main.py`**: Core application with all API endpoints and business logic
- **`models.py`**: Defines the database table structure using SQLAlchemy ORM
- **`schemas.py`**: Pydantic models for request/response validation
- **`database.py`**: Database engine and session configuration
- **`requirements.txt`**: List of Python package dependencies

---

## 🗄️ Database Schema

The API uses SQLite by default. The database contains a single `events` table:

### Events Table

| Column        | Type     | Description                          |
|---------------|----------|--------------------------------------|
| `id`          | INTEGER  | Primary key (auto-increment)         |
| `user_id`     | VARCHAR  | User identifier (indexed)            |
| `event_type`  | VARCHAR  | Event category/type (indexed)        |
| `timestamp`   | DATETIME | Event creation time (UTC, indexed)   |
| `metadata`    | JSON     | Flexible additional data             |

**Indexes:**
- Primary key on `id`
- Index on `user_id` for fast user lookups
- Index on `event_type` for fast type filtering
- Index on `timestamp` (implicit) for time-based queries

---

## ⚙️ Configuration

### Database Configuration

By default, the API uses SQLite. To use a different database:

1. **Edit `database.py`:**
   ```python
   # For PostgreSQL
   DATABASE_URL = "postgresql://user:password@localhost/dbname"
   
   # For MySQL
   DATABASE_URL = "mysql+pymysql://user:password@localhost/dbname"
   ```

2. **Install appropriate driver:**
   ```bash
   # PostgreSQL
   pip install psycopg2-binary
   
   # MySQL
   pip install pymysql
   ```

### Server Configuration

Customize server settings when running:

```bash
# Change port
uvicorn main:app --port 8080

# Change host (for external access)
uvicorn main:app --host 0.0.0.0

# Production mode (no reload)
uvicorn main:app --workers 4
```

---

## 🧪 Testing the API

### Manual Testing

Use the interactive docs at http://localhost:8000/docs to test all endpoints visually.

### Automated Testing

Create a test script:

```python
import requests
import time

BASE_URL = "http://localhost:8000"

# Test 1: Create events
print("Creating test events...")
for i in range(5):
    requests.post(f"{BASE_URL}/events/", json={
        "user_id": f"user_{i % 3}",
        "event_type": ["login", "click", "purchase"][i % 3],
        "metadata": {"test": True, "index": i}
    })
    time.sleep(0.1)

# Test 2: Get statistics
print("\nGetting statistics...")
stats = requests.get(f"{BASE_URL}/stats/total").json()
print(f"Total events: {stats['total_events']}")

# Test 3: Get events by type
print("\nEvents by type:")
by_type = requests.get(f"{BASE_URL}/stats/by-event-type").json()
for item in by_type:
    print(f"  {item['event_type']}: {item['count']}")
```

---

## 🚀 Production Deployment

For production deployment:

1. **Use PostgreSQL** instead of SQLite
2. **Add authentication** (JWT tokens, API keys)
3. **Enable CORS** if needed for web clients
4. **Set up monitoring** and logging
5. **Use environment variables** for configuration
6. **Run with multiple workers**: `uvicorn main:app --workers 4`

### Deployment Platforms

- **Render.com** - Easy deployment with free tier
- **Railway.app** - Simple setup, generous free tier
- **Fly.io** - Global deployment
- **AWS/GCP/Azure** - Enterprise-grade scaling

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guidelines
- Add docstrings to all functions
- Update README.md if needed
- Test your changes thoroughly

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Ramiro Boccuzzi (Cuzzi)**

- GitHub: [@Cuzzi-i](https://github.com/Cuzzi-i)
- LinkedIn: [Ramiro Boccuzzi](https://www.linkedin.com/in/boccuzziramiroa/)

---

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework
- Database ORM by [SQLAlchemy](https://www.sqlalchemy.org/) - The Python SQL toolkit
- Data validation by [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation using Python type hints
- Inspired by modern analytics platforms and event tracking systems

---

## 📞 Support

If you have questions or run into issues:

- **Open an issue**: [GitHub Issues](https://github.com/Cuzzi-i/stadistics-by-cuzzi/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Cuzzi-i/stadistics-by-cuzzi/discussions)

---

## ⭐ Show Your Support

If you find this project useful, please consider giving it a star on GitHub! It helps others discover the project.

---

## 🗺️ Roadmap

Future improvements planned:

- [ ] Add authentication and authorization
- [ ] Implement rate limiting
- [ ] Add data export functionality (CSV, JSON)
- [ ] Create visualization dashboard
- [ ] Add real-time WebSocket updates
- [ ] Implement event batching for high-volume scenarios
- [ ] Add data retention policies
- [ ] Create Docker container for easy deployment

---

**Built by Ramiro Boccuzzi**