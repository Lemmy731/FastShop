FastShop - Backend API with Python and Flask
FastShop is a backend API developed with Python and Flask, focusing on a simple and user-friendly structure for managing user authentication and product management. This project demonstrates a  RESTful API that integrates features like user registration and login, secure token-based authentication, and CRUD operations for product management. FastShop uses SQLite as its database, making it lightweight and easy to set up locally.

Table of Contents
Features
Tech Stack
Project Structure
Getting Started
Installation
Configuration
Running the Application
API Endpoints
Database Schema
Presentations
Future Improvements
Features
User Authentication: Secure registration and login system with JWT token-based authentication.
Product Management: CRUD operations for product management, allowing users to create, read, update, and delete product entries.
Database: Uses SQLite for data storage, making it simple to deploy and test.
Tech Stack
Backend Framework: Python with Flask
Database: SQLite
Authentication: JSON Web Tokens  for secure, stateless authentication.
Project Structure

FastShop/
├── app.py               # Main application entry point
├── config.py            # Application configuration
├── models.py            # Database models for Users and Products
├── auth.py              # Routes and logic for authentication (signup, login)
├── product.py           # Routes and logic for product CRUD operations
├── __init__.py          # Initialization of app components and Blueprints
├── requirements.txt     # Required packages
└── .env                 # Environment variables (e.g., SECRET_KEY)
Getting Started
Installation
Clone the repository:

git clone https://github.com/Lemmy731/FastShop.git
cd FastShop
Create a virtual environment and install dependencies:

bash
Copy code
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
Configuration
Environment Variables: Create a .env file with the following structure:

makefile
Database Initialization: The database file will be created automatically when you run the app.

Running the Application
Start the application by running:

bash
Copy code
python app.py
The server should now be running on http://127.0.0.1:5000/.

API Endpoints
POST /auth/signup - Registers a new user
Payload: { "fullname": "User Name", "email": "user@example.com", "password": "password123" }
POST /auth/login - Authenticates a user and returns a JWT token
Payload: { "email": "user@example.com", "password": "password123" }
Products
GET /products - Retrieves a list of products
GET /products/<id> - Retrieves details of a product by ID
POST /products - Creates a new product
Payload: { "name": "Product Name", "price": 29.99, "description": "Product description" }
PUT /products/<id> - Updates an existing product
Payload: { "name": "Updated Product", "price": 34.99, "description": "Updated description" }
DELETE /products/<id> - Deletes a product by ID
Database Schema
User:

id (Primary Key)
fullname (String)
email (Unique, String)
password (Hashed String)
Product:
id (Primary Key)
name (String)
price (Float)
description (String)
Presentations
Project Presentation: https://docs.google.com/presentation/d/14cYEAgX_PK1cmsH30GIx5E032NRZXb37HWZCjz2zqsc/edit?usp=drive_link
Video Presentation: https://www.loom.com/share/5bafd9bd593142f0b99af2ed48b7586f?sid=2efef86d-da1a-4e3b-b7ca-827ac2c0eb90
Future Improvements
User Roles: Adding role-based access for admin and general users.
Pagination: For product listings to improve performance.
Enhanced Security: Improve token management and password security mechanisms.



