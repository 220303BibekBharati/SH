# E-Commerce Website

A fully functional e-commerce website built with Django.

## Features

- User registration and authentication
- Product catalog with categories
- Shopping cart
- Checkout process
- Order management
- Payment processing (dummy)
- Admin panel for management

## Installation

1. Clone the repository
2. Navigate to the project directory: `cd ecommerce_project`
3. Install dependencies: `pip install -r requirements.txt`
4. Run migrations: `python manage.py makemigrations` then `python manage.py migrate`
5. Create a superuser: `python manage.py createsuperuser`
6. (Optional) Populate sample data: `python manage.py populate_db`
7. Run the server: `python manage.py runserver`

## Usage

- Access the website at `http://127.0.0.1:8000/`
- Admin panel at `http://127.0.0.1:8000/admin/`

## Technologies Used

- Django 4.2.7
- Bootstrap 5
- SQLite (or PostgreSQL)
- Stripe (for payments, test mode)