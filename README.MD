# Finance System API

A Python Django REST API backend for managing personal financial records.
Built with Django 6.0, Django REST Framework, and JWT authentication.


## Tech Stack

| Technology | Purpose |
| Python 3.12 | Core language |
| Django 6.0 | Web framework |
| Django REST Framework | API development |
| SimpleJWT | JWT authentication |
| SQLite | Database |
| django-filter | Query filtering |

## Features

- JWT based user authentication
- Role based access control (Viewer / Analyst / Admin)
- Full CRUD for financial transactions (income and expenses)
- Category management
- Filter transactions by type, category, date range, keyword
- Financial analytics — summary, category breakdown, monthly totals
- Soft delete for transactions
- Global error handling with consistent JSON responses
- Input validation with descriptive error messages
- Unit tests for all core features

## Project Structure
```
finance_system/
├── apps/
│   ├── users/           → authentication and user management
│   ├── transactions/    → financial records CRUD
│   └── analytics/       → summaries and reports
├── config/              → Django settings and URL routing
├── manage.py
├── requirements.txt
└── README.md
```

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/finance-system.git
cd finance-system
```

### 2. Create and activate virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create `.env` file in root folder
```
SECRET_KEY=your-secret-key-here
DEBUG=True
```

### 5. Run migrations
```bash
python manage.py migrate
```

### 6. Create superuser
```bash
python manage.py createsuperuser
```

### 7. Run the server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/`

## API Endpoints

### Authentication
| Method | Endpoint | Description | Auth Required |

| POST | `/api/auth/register/` | Register new user | No |
| POST | `/api/auth/login/` | Login and get JWT token | No |
| GET | `/api/auth/profile/` | Get logged in user profile | Yes |

### Transactions
| Method | Endpoint | Description | Auth Required |

| GET | `/api/transactions/` | List my transactions | Yes |
| POST | `/api/transactions/` | Create new transaction | Yes |
| GET | `/api/transactions/<id>/` | Get single transaction | Yes |
| PUT | `/api/transactions/<id>/` | Update transaction | Yes |
| DELETE | `/api/transactions/<id>/` | Soft delete transaction | Yes |
| GET | `/api/transactions/categories/` | List categories | Yes |
| POST | `/api/transactions/categories/` | Create category (admin only) | Yes |

### Filters (add to GET /api/transactions/)
| Parameter | Example | Description |

| `type` | `?type=expense` | Filter by income or expense |
| `category` | `?category=1` | Filter by category ID |
| `date_from` | `?date_from=2025-01-01` | Transactions from this date |
| `date_to` | `?date_to=2025-01-31` | Transactions up to this date |
| `search` | `?search=lunch` | Search in notes |

### Analytics
| Method | Endpoint | Description | Auth Required |

| GET | `/api/analytics/summary/` | Total income, expenses, balance | Analyst/Admin |
| GET | `/api/analytics/category-breakdown/` | Spending per category | Analyst/Admin |
| GET | `/api/analytics/monthly/` | Month by month totals | Analyst/Admin |
| GET | `/api/analytics/recent/` | Last 5 transactions | Yes |



## User Roles

| Role | Permissions |
|---|---|
| Viewer | View transactions only |
| Analyst | View transactions + access all analytics |
| Admin | Full access — create, update, delete, manage categories |



## How to Use the API

### Step 1 — Register
```json
POST /api/auth/register/
{
    "username": "john",
    "password": "mypassword123",
    "email": "john@example.com",
    "role": "admin"
}
```

### Step 2 — Login and copy the access token
```json
POST /api/auth/login/
{
    "username": "john",
    "password": "mypassword123"
}
```

### Step 3 — Use token in all future requests
```
Header: Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

### Step 4 — Create a transaction
```json
POST /api/transactions/
{
    "amount": "5000.00",
    "transaction_type": "income",
    "category": 1,
    "date": "2025-01-15",
    "notes": "January salary"
}
```

### Step 5 — View analytics
```
GET /api/analytics/summary/
```


## Running Tests
```bash
python manage.py test apps.users apps.transactions apps.analytics
```

Expected output:
```
Ran 10 tests in 2.3s
OK
```



## Assumptions Made

- Soft delete is used for transactions — records are marked `is_deleted=True` rather than permanently removed. This preserves financial history.
- JWT access tokens expire after 24 hours. Refresh tokens expire after 7 days.
- Category creation is restricted to admin users only. All users can view categories.
- Analytics endpoints are restricted to analyst and admin roles. Viewers can only access transaction records.
- Amount must be greater than zero. Transaction date cannot be in the future.
- SQLite is used for simplicity as this is an assessment project. Can be swapped for PostgreSQL in production by updating the DATABASE setting.


## Admin Panel

Django's built-in admin panel is available at:
```
http://127.0.0.1:8000/admin/
```

Login with superuser credentials to manage all data visually.
