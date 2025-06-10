# 🧺 Laundry Management System API

A RESTful API for managing a multi-tenant laundry service platform, built using **Django** and **Django REST Framework**. This system supports companies managing their customers, employees, laundry services, orders, invoices, and payments.

---

## 🚀 Features

- ✅ Multi-tenant company support
- ✅ Role-based access control (Admin, Staff)
- ✅ Customer & employee management
- ✅ Laundry service catalog with pricing
- ✅ Order and invoice management
- ✅ Payment recording
- ✅ Token-based authentication
---

## 🛠 Tech Stack

- **Backend**: Python, Django, Django REST Framework  
- **Database**: PostgreSQL (or SQLite for local use)  
- **Authentication**: JWT or Token Auth (Django REST)  

---

## 📦 Installation Guide

### 1. Clone the Repository

```bash
git clone https://github.com/berndoe/laundry-system-api.git
cd laundry-system-api
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create `.env` File

Create a `.env` file in the root directory with contents similar to:

```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://user:password@localhost:5432/laundrydb
```

### 5. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Start the Development Server

```bash
python manage.py runserver
```

---

## 🔐 Authentication

This API uses token-based authentication (JWT or Token Auth).

### Obtain Token

```
POST /api//
{
  "username": "your_username",
  "password": "your_password"
}
```

### Use Token

Add this to the header for any authenticated request:

```
Authorization: Bearer <your_token>
```

---

## 📖 API Endpoints Overview

| Method | Endpoint                        | Description                          |
|--------|----------------------------------|--------------------------------------|
| GET    | /api/companies/                 | List companies (admin only)         |
| POST   | /api/companies/                 | Create a new company                 |
| GET    | /api/company/customers          | List all customers for a company     |
| POST   | /api/company/customers/         | Add a new customer                   |
| GET    | /api/employees/                 | List all employees for a company     |
| POST   | /api/employees/                 | Add a new employee                   |
| GET    | /api/services/                  | List available laundry services      |
| POST   | /api/orders/                    | Create a new laundry order           |
| GET    | /api/invoices/                  | View generated invoices              |
| POST   | /api/payments/                  | Record payment against invoice       |

> ✅ API is fully RESTful and uses standard HTTP response codes.

---

## 🧾 Data Models

- **Company** – Tenant model
- **Customer** – Belongs to a company
- **Employee** – Belongs to a company
- **ServiceItem** – Laundry service types and prices
- **Order** – Contains one or more order items
- **OrderItems** – Contains one or more service items
- **Invoice** – Auto-generated from completed orders
- **Payment** – Linked to invoice
- **User** – Optional: Separate from employee (if needed)

---

## ✅ Example Use Case

1. Admin creates a company.
2. Company staff adds customers and services.
3. Orders are created for customers.
4. Invoices are auto-generated.
5. Payments are recorded.
6. Reports show total revenue, orders, etc.

---

## 🧰 Tools

- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL](https://www.postgresql.org/)

---

## 📄 License

This project is licensed under the MIT License. See `LICENSE` file for details.

---

## Contributing

Contributions, bug reports, and suggestions are welcome!

1. Fork the repository
2. Create a new branch
3. Submit a pull request
