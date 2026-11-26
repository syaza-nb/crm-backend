# CRM Platform – Backend

A multi-user Customer Relationship Management (CRM) platform inspired by HubSpot, developed using Python, FastAPI and PostgreSQL.

## Overview

The CRM Platform helps businesses manage customer relationships, sales opportunities, teams and daily activities through a centralised system.

The backend provides RESTful APIs to support the frontend application.

## Technology Stack

- **Language:** Python
- **Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Database Migrations:** Alembic
- **Authentication:** JWT
- **Validation:** Pydantic
- **API Documentation:** Swagger UI

## Core Modules

1. User Authentication and Role Management
2. Contacts Management
3. Companies Management
4. Sales Pipeline and Deals
5. Tasks and Activities
6. Dashboard and Reports

## User Roles

| Role | Permissions |
|---|---|
| Admin | Full system access |
| Sales Manager | Manages team records and monitors sales performance |
| Sales Representative | Manages assigned records |

## Project Structure

```text
backend/
├── app/
│   ├── api/
│   │   └── routes/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── main.py
├── tests/
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Local Development Setup

### 1. Clone the repository

```bash
git clone YOUR_BACKEND_REPOSITORY_URL
cd backend
```

### 2. Create a virtual environment

```bash
py -m venv .venv
```

### 3. Activate the virtual environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the backend root directory.

Configure the following variables:

```env
APP_NAME=CRM Platform API
APP_VERSION=1.0.0
DEBUG=True

DB_HOST=localhost
DB_PORT=5432
DB_NAME=crm_platform
DB_USER=postgres
DB_PASSWORD=your_password
```

### 6. Run the development server

```bash
python -m uvicorn app.main:app --reload
```

## API Documentation

Once the server is running:

- Swagger UI: http://127.0.0.1:8000/docs
- Health Check: http://127.0.0.1:8000/health

## Project Status

Backend foundation and initial application configuration completed. Database integration and CRM modules are under development.

## Author

Developed as a personal software development project.