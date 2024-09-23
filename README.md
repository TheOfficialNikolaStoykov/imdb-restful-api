
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
- PostgreSQL

## Database Setup

### Restore the Database from Backup

This project uses a pre-existing database that you can restore using the provided `full_backup.sql` file. Follow the instructions below to restore the database.

#### Prerequisites:
- Make sure PostgreSQL (or your chosen database system) is installed and running.
- You have created a PostgreSQL database where the backup will be restored. You can create a new one using the following command:

    ```bash
    createdb <your_database_name>
    ```

#### Steps to Restore the Database

1. **Locate the `full_backup.sql` file**:
   The `full_backup.sql` file is included in this repository. Ensure that it is in the root folder or accessible from where you are running the command.

2. **Restore the database**:
   To restore the database, use the following command:

    ```bash
    psql -U <your_username> -d <your_database_name> -f full_backup.sql
    ```

   - `<your_username>`: Replace this with your PostgreSQL username.
   - `<your_database_name>`: Replace this with the name of the database you created for the project.
   
   Example:

    ```bash
    psql -U postgres -d imdb_db -f full_backup.sql
    ```

   This command will restore the database schema and data from the `full_backup.sql` file.

#### Database Configuration in Django

Ensure that your `settings.py` file is properly configured with your PostgreSQL credentials.

Open `cinebase/settings.py` and modify the `DATABASES` settings as follows:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '<your_database_name>',
        'USER': '<your_username>',
        'PASSWORD': '<your_password>',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

After restoring the database, run the following commands to apply any outstanding migrations:
```python
python manage.py migrate
```

## Project Setup

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
