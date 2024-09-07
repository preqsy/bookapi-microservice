# Library Management API

This project is a library management system designed to allow users to browse the catalog of books, borrow them, and manage library operations. It consists of two independent API services: a Frontend API for users and a Backend/Admin API for administrators.

## Features

### Frontend API:

- Enroll users into the library using their email, first name, and last name.
- List all available books.
- Get a single book by its ID.
- Filter books by publishers and categories.
- Borrow books by specifying the duration in days.

### Admin API:

- Add new books to the catalog.
- Remove books from the catalog.
- Fetch/list users enrolled in the library.
- Fetch/list users and the books they have borrowed.
- Fetch/list books that are currently unavailable for borrowing.

## Technologies Used

- **FastAPI**: For building RESTful API endpoints.
- **Pydantic**: For data validation and serialization.
- **SQLAlchemy**: ORM for database modeling and interaction.
- **PostgreSQL**: Database management.
- **Docker**: For containerizing the services.
- **Requests**: For making HTTP requests between the frontend and admin services.
- **pytest**: For automated testing.
- **Poetry**: For dependency management.

## Getting Started

### Prerequisites

- Python 3.10+
- Docker (for containerization)

### Installation

1. **Clone the repository**:

   ```sh
   git clone https://github.com/preqsy/bookapi-microservice.git
   cd bookapplication
   ```

2. **Install Poetry**:
   Follow the instructions at [Poetry's official documentation](https://python-poetry.org/docs/#installation) to install Poetry.

3. **Install dependencies**:

   ```sh
   poetry install
   ```

4. **Set up the database**:
   Create PostgreSQL databases for both the frontend and admin services, and configure the connections in the `.env` files located in `frontend-api/.env` and `admin-api/.env`.

   Example for `.env`:

   ```
   SQLALCHEMY_DATABASE_URL=postgresql://user:password@localhost:5432/book_admin
   ```

5. **Run the application**:
   Use Docker Compose to start both the frontend and admin services:

   ```sh
   docker-compose up --build
   ```

   The Frontend API will be available at `http://localhost:8001` and the Admin API at `http://localhost:8000`.

### Running Tests

1. **Install `pytest`**:

   ```sh
   poetry add pytest --dev
   ```

2. **Add Your Test Database URL**:

3. **Run the tests**:
   ```sh
   poetry run pytest
   ```

### Running with Docker

1. **Build the Docker images**:

   ```sh
   docker-compose build
   ```

2. **Run the Docker containers**:

   ```sh
   docker-compose up
   ```

3. **Access the services**:
   - Frontend API: `http://localhost:8001`
   - Admin API: `http://localhost:8000`

## Project Structure

```
bookapplication/
├── admin-api/              # Admin API service
│   ├── endpoints/          # Admin API endpoints
│   ├── models/             # Admin API models
│   ├── schemas/            # Admin API schemas
│   └── main.py             # Admin API entry point
├── frontend-api/           # Frontend API service
│   ├── endpoints/          # Frontend API endpoints
│   ├── models/             # Frontend API models
│   ├── schemas/            # Frontend API schemas
│   └── main.py             # Frontend API entry point
├── docker-compose.yml      # Docker Compose file
├── pyproject.toml          # Poetry configuration file
└── README.md               # Project documentation
```

## Contribution

Contributions are welcome! Please create a pull request or raise an issue for any bugs or feature requests.

## License

This project is licensed under the MIT License.

## Contact

For more information, please contact [obbyprecious24@gmail.com](mailto:obbyprecious24@gmail.com).
