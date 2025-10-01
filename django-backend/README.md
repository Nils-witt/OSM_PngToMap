# PngToMap Django API Backend

This Django project provides a REST API with WebSocket support for the PngToMap application.

## Features

- **Django REST Framework**: Full REST API support with browsable API
- **WebSocket Support**: Real-time communication using Django Channels
- **CORS Headers**: Configured for frontend integration
- **Authentication**: Built-in Django authentication system
- **Redis Channel Layer**: For WebSocket message passing (requires Redis)

## Setup

### Prerequisites

- Python 3.8+
- Redis server (for WebSocket support)

### Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run migrations:
   ```bash
   python manage.py migrate
   ```

3. Create a superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```

4. Start Redis server:
   ```bash
   redis-server
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   # or use the provided script
   ./start_server.sh
   ```

## API Endpoints

### REST API

- `GET /api/v1/public-health/` - Public health check (no auth required)
- `GET /api/v1/health/` - Protected health check (auth required)
- `GET /api/v1/users/` - List users (auth required)
- `POST /api/v1/send-message/` - Send WebSocket message (auth required)
- `/api-auth/` - Django REST Framework authentication endpoints

### WebSocket

- `ws://localhost:8000/ws/api/<room_name>/` - WebSocket connection

## WebSocket Usage

Connect to a WebSocket room and send/receive messages:

```javascript
const socket = new WebSocket('ws://localhost:8000/ws/api/test/');

socket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log('Message:', data);
};

socket.send(JSON.stringify({
    'message': 'Hello World!',
    'type': 'message'
}));
```

## Configuration

Key settings in `pngtomap_api/settings.py`:

- **CORS_ALLOWED_ORIGINS**: Configure allowed frontend origins
- **CHANNEL_LAYERS**: Redis configuration for WebSockets
- **REST_FRAMEWORK**: API configuration and permissions

## Development

The project includes:

- Default superuser: `admin` / `admin123`
- Browsable API at `/api/v1/`
- Admin interface at `/admin/`
- API documentation via Django REST Framework

## Project Structure

```
django-backend/
├── manage.py
├── requirements.txt
├── start_server.sh
├── pngtomap_api/          # Main project configuration
│   ├── settings.py        # Django settings with REST/WebSocket config
│   ├── urls.py           # Main URL configuration
│   ├── wsgi.py           # WSGI configuration
│   └── asgi.py           # ASGI configuration for WebSockets
└── api/                   # API application
    ├── views.py          # API views and endpoints
    ├── urls.py           # API URL patterns
    ├── serializers.py    # DRF serializers
    ├── consumers.py      # WebSocket consumers
    ├── routing.py        # WebSocket URL routing
    └── models.py         # Database models (extend as needed)
```