# geo-api-django
Django backend application for working with geo-points

# GeoPoints API - Geographic Points Management (Django Backend)

A Django backend API for managing geographic points on a map, allowing users to create points, send messages, and search for points within a specified radius from given coordinates.

## Table of Contents

- [Technology Stack](#technology-stack)
- [Installation and Setup](#installation-and-setup)
- [API Endpoints](#api-endpoints)
- [Request Examples](#request-examples)
- [Testing](#testing)
- [For Developers](#for-developers)

## Technology Stack

- **Backend Framework**: Django 5+
- **API**: Django REST Framework (DRF)
- **Database**: PostgreSQL with PostGIS (recommended) / SQLite
- **Geo Features**: GeoDjango
- **Language**: Python 3.10+
- **Authentication**: Token Authentication
- **Testing**: pytest

## Installation and Setup

### Prerequisites

For **Ubuntu/Debian**:
```bash
sudo apt-get update
sudo apt-get install -y binutils libproj-dev gdal-bin libgdal-dev
```

For **macOS**:
```bash
brew install gdal geos proj
```

### Steps

1. **Clone the Repository**:
   ```bash
   https://github.com/moonPrTea/geo-api-django.git
   cd geo-api-django
   ```

2. **Setup Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Configuration**:
   - **Option A: SQLite (for development)**:
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```
   - **Option B: PostgreSQL with PostGIS**:
     ```sql
     CREATE DATABASE geopoints_db;
     CREATE USER geopoints_user WITH PASSWORD 'your_password';
     ALTER ROLE geopoints_user SET client_encoding TO 'utf8';
     GRANT ALL PRIVILEGES ON DATABASE geopoints_db TO geopoints_user;
     ```
     Update `DATABASES` in `settings.py`:
     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.contrib.gis.db.backends.postgis',
             'NAME': 'name',
             'USER': 'user',
             'PASSWORD': 'password',
             'HOST': 'host',
             'PORT': 'port',
         }
     }
     ```
     Run migrations:
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```

5. **Create Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Server**:
   ```bash
   python manage.py runserver
   ```

   Server will be available at: [http://localhost:8000](http://localhost:8000).

---

## API Endpoints

### Authentication

| Method | Endpoint               | Description              |
|--------|------------------------|--------------------------|
| POST   | `/api/accounts/login`   | Get authentication token |
| POST   | `/api/accounts/logout`  | Logout from the system   |

### Points

| Method | Endpoint                | Description                       |
|--------|-------------------------|-----------------------------------|
| POST   | `/api/points`            | Create new geographic point      |
| GET    | `/api/points/search`     | Search points within a radius    |

### Messages

| Method | Endpoint                  | Description                   |
|--------|---------------------------|-------------------------------|
| POST   | `/api/points/messages`     | Create a message for a point  |

---

## Request Examples

### 1. Get Authentication Token

**HTTP Request:**
```http
POST /api/accounts/login HTTP/1.1
Content-Type: application/json

{
    "username": "example",
    "password": "example_password"
}
```

**CURL Command:**
```bash
curl -X POST http://localhost:8000/api/accounts/login \
  -H "Content-Type: application/json" \
  -d '{"username": "example", "password": "example_password"}'
```

**Response:**
```json
{
    "token": "33152b683034571063c42b50aac1bca0fe0c3563"
}
```

---

### 2. Create Geographic Point

**HTTP Request:**
```http
POST /api/points HTTP/1.1
Authorization: Token 33152b683034571063c42b50aac1bca0fe0c3563
Content-Type: application/json

{
    "title": "Example point",
    "latitude": 38.1212,
    "longitude": 12.321
}
```

**CURL Command:**
```bash
curl -X POST http://localhost:8000/api/points \
  -H "Authorization: Token 33152b683034571063c42b50aac1bca0fe0c3563" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Example point",
    "latitude": 38.1212,
    "longitude": 12.321
  }'
```

**Response:**
```json
{
    "message": "point successfully created",
    "object": {
        "id": 1,
        "title": "Example point",
        "latitude": 38.1212,
        "longitude": 12.321,
        "creator": "example",
        "created_at": "2026-01-08T20:15:47.123231Z"
    }
}
```

---

### 3. Search Points in Radius

**HTTP Request:**
```http
GET /api/points/search?latitude=38.1212&longitude=12.321&radius=2 HTTP/1.1
Authorization: Token 33152b683034571063c42b50aac1bca0fe0c3563
```

**CURL Command:**
```bash
curl -X GET "http://localhost:8000/api/points/search?latitude=38.1212&longitude=12.321&radius=2" \
  -H "Authorization: Token 33152b683034571063c42b50aac1bca0fe0c3563"
```

**Response:**
```json
{
    "params": {
        "latitude": 38.1212,
        "longitude": 12.321,
        "radius": "2.0 km"
    },
    "count_points": 1,
    "points": [
        {
            "latitude": 38.1212,
            "longitude": 12.321,
            "distance": 0.0,
            "title": "Example point",
            "creator": "example",
            "created_at": "2026-01-08T20:15:47.123231Z"
        }
    ]
}
```

---

### 4. Create Message for Point

**HTTP Request:**
```http
POST /api/points/messages HTTP/1.1
Authorization: Token 33152b683034571063c42b50aac1bca0fe0c3563
Content-Type: application/json

{
    "message_text": "Amazing place to spend time with your family",
    "id_point": 1
}
```

**CURL Command:**
```bash
curl -X POST http://localhost:8000/api/points/messages \
  -H "Authorization: Token 33152b683034571063c42b50aac1bca0fe0c3563" \
  -H "Content-Type: application/json" \
  -d '{
    "message_text": "Amazing place to spend time with your family",
    "id_point": 1
  }'
```

**Response:**
```json
{
    "message": "message successfully created",
    "object": {
        "id": 1,
        "id_point": 1,
        "point_title": "Example point",
        "point_coordinates": "38.121200, 12.32100",
        "creator_username": "example",
        "message_text": "Amazing place to spend time with your family",
        "created_at": "2026-01-08T20:15:47.123231Z",
        "updated_at": "2026-01-08T20:15:55.322121Z"
    }
}
```

---

### 5. Logout

**HTTP Request:**
```http
POST /api/accounts/logout HTTP/1.1
Authorization: Token 33152b683034571063c42b50aac1bca0fe0c3563
```

**CURL Command:**
```bash
curl -X POST http://localhost:8000/api/accounts/logout \
  -H "Authorization: Token 33152b683034571063c42b50aac1bca0fe0c3563"
```

**Response:**
```json
{
    "message": "logged out successfully"
}
```

## Testing

Run tests with **pytest**:

```bash
# Run all tests
pytest

# Run specific test module
pytest geoapi/tests/test_views.py

# Run with coverage report
pytest --cov=geoapi
```

---

## For Developers

### Project Structure
```
geopoints-api/
├── config/
│   ├── asgi.py     # DJANGO_SETTINGS_MODULE 
│   ├── env.py      # env functions
│   ├── settings.py # app settings
│   ├── urls.py     # URL routing
│   └── wsgi.py      # WSGI config for config project
├── geoapi/
│   ├── models.py       # data models (Point, Message)
│   ├── apps.py    # app config
│   ├── admin.py    # admin models
│   ├── serializers/    # serializers
│   ├── views/          # ApiView classes
│   └── tests/          # Test files
├── manage.py
├── requirements.txt
└── README.md
```

### Geographic Data Validation

- Coordinates are validated for correct ranges:
  - **Latitude**: -90 to 90
  - **Longitude**: -180 to 180
  - Distance calculations are made in kilometers.
  - Spatial indexing is used for performance optimization.
  - Coordinate system is SRID 4326 (WGS84).


## Error Handling

The API returns appropriate HTTP status codes based on the result of the request. Here are the possible status codes:

| **Status Code** | **Description**                                   |
|-----------------|---------------------------------------------------|
| `200`           | Success                                           |
| `400`           | Bad Request (e.g., validation errors)             |
| `401`           | Unauthorized (authentication required)           |
| `404`           | Not Found                                         |
| `500`           | Internal Server Error                             |

---

## Notes

- **Radius**: The radius for searching points is provided in kilometers.
  
- **GeoDjango**: All requests related to geographic points utilize GeoDjango for handling geographic data.

- **PostGIS**: PostGIS is used to extend PostgreSQL, enabling spatial queries and efficient management of geographic points on the map.

## Deployment

### Production Considerations

1. **Set DEBUG to False** in settings.py
2. **Use PostgreSQL with PostGIS** in production
3. **Use environment variables** for sensitive data