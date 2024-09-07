Library Management System
This repository contains two independent API services for managing a library system.

Frontend API: Allows users to browse available books, filter by categories/publishers, and borrow books.
Admin API: Enables admins to add or remove books, list enrolled users, and manage borrowed books.
Features
Frontend API:
Enroll users into the library
List all available books
Filter books by category or publisher
Borrow books by ID
Admin API:
Add new books to the catalog
Remove books from the catalog
Fetch users and books they have borrowed
List unavailable books with return dates
Tech Stack
Python: FastAPI framework for building APIs
PostgreSQL: For storing book and user data
Docker: Containerized deployment
Poetry: Dependency management
Requests: For communication between services
Installation
Clone the repository:
bash
Copy code
git clone https://github.com/yourusername/library-management.git
cd library-management
Ensure you have Docker installed.
Build and start the services:
bash
Copy code
docker-compose up --build
API Endpoints
Frontend API (runs on port 8001):
GET /books/get-all: List all available books
POST /books/category: Filter books by category
POST /books/publisher: Filter books by publisher
POST /books/{id}/borrow: Borrow a book by ID
Admin API (runs on port 8000):
POST /books/: Add a new book
DELETE /books/{id}: Remove a book
GET /books/: List all books
GET /books/{id}: Get book by ID
License
This project is licensed under the MIT License.
