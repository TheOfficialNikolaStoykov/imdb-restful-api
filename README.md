
# IMDB RESTful API

This project is a RESTful API for managing media content, users, reviews, and streaming platforms. The API is built using Django Rest Framework (DRF) and includes features like user authentication, pagination, filtering, and throttling.

## Features

- **Media Management**: Create, retrieve, update, and delete media objects (like movies and series) with detailed information.
- **Streaming Platforms**: Perform CRUD operations on streaming platforms.
- **Review System**: Registered users can create, update, delete, and list reviews for media objects.
- **User Management**: Supports user registration, login, and logout with token-based authentication.
- **Rate Limiting**: Throttling is applied for anonymous and authenticated users for specific API views.
- **Filtering**: Filter reviews based on the reviewer's username and activity status.

## Setup Instructions

### Prerequisites

- Python 3.11 or higher
- Django 4.x or higher
- Virtual environment setup (venv)

### Step-by-Step Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/cinebase.git
   ```

2. Navigate to the project directory:

   ```bash
   cd cinebase
   ```

3. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate    # On Windows use `venv\Scripts\activate`
   ```

4. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Run migrations to set up the database schema:

   ```bash
   python manage.py migrate
   ```

6. Create a superuser to access the Django admin panel:

   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:

   ```bash
   python manage.py runserver
   ```

8. Open the browser and navigate to `http://127.0.0.1:8000/` to access the API.

### API Documentation

API documentation is available via Swagger UI. You can access it [here](https://theofficialnikolastoykov.github.io/imdb-restful-api/).

For example:

```
http://127.0.0.1:8000/swagger/
```

### Running Tests

To run tests, use the following command:

```bash
python manage.py test
```

To run coverage, use the following commands sequentially:
```bash
coverage run manage.py test
```
```bash
coverage report
```

## Technologies Used

- **Backend Framework**: Django REST Framework
- **Database**: PostgreSQL
- **API Documentation**: Swagger UI

## License

This project is licensed under the MIT License - see the LICENSE file for details.
