# E-commerce Microservices

A Django-based microservices architecture for a simple e-commerce system consisting of three services:

1. **User Service** (Port 8000) - Handles user authentication and profiles
2. **Product Service** (Port 8001) - Manages product catalog and inventory
3. **Order Service** (Port 8002) - Handles orders and coordinates with other services

## Architecture

```
┌─────────────────┐    HTTP/JSON    ┌──────────────────┐
│   User Service  │◄───────────────►│  Product Service │
│   Port: 8000    │                 │   Port: 8001     │
└─────────────────┘                 └──────────────────┘
         ▲                                    ▲
         │                                    │
         │            HTTP/JSON               │
         │                                    │
         ▼                                    ▼
┌─────────────────────────────────────────────────────┐
│                Order Service                        │
│                Port: 8002                          │
└─────────────────────────────────────────────────────┘
```

## Setup Instructions


### 1. Manual Setup (Alternative)
If you prefer manual setup:

```bash
# User Service
cd user_service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
opentelemetry-bootstrap --action=install
python manage.py makemigrations
python manage.py migrate
#set env var
# Environment variables for User Service
export OTEL_RESOURCE_ATTRIBUTES="service.name=user_service,service.version=1.0.0,deployment.environment=development,db.system=sqlite,db.name=user_service_db,db.connection_string=sqlite:///db_user_service.sqlite3"
export OTEL_EXPORTER_OTLP_ENDPOINT="http://127.0.0.1:4318"
export OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
export DJANGO_SETTINGS_MODULE=user_service.settings
deactivate

# Product Service
cd ../product_service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
opentelemetry-bootstrap --action=install
python manage.py makemigrations
python manage.py migrate
#set env var
export OTEL_RESOURCE_ATTRIBUTES="service.name=product_service,service.version=1.0.0,deployment.environment=development,db.system=sqlite,db.name=product_service_db,db.connection_string=sqlite:///db_product_service.sqlite3"
export OTEL_EXPORTER_OTLP_ENDPOINT="http://127.0.0.1:4318"
export OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
export DJANGO_SETTINGS_MODULE=product_service.settings
deactivate

# Order Service
cd ../order_service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
opentelemetry-bootstrap --action=install
python manage.py makemigrations
python manage.py migrate
#set env var
export OTEL_RESOURCE_ATTRIBUTES="service.name=order_service,service.version=1.0.0,deployment.environment=development,db.system=sqlite,db.name=order_service_db,db.connection_string=sqlite:///db_order_service.sqlite3,peer.service=order_service_db"
export OTEL_EXPORTER_OTLP_ENDPOINT="http://127.0.0.1:4318"
export OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
export DJANGO_SETTINGS_MODULE=order_service.settings
deactivate
```

### 2. Run Services


#### Option A: Manual startup (open three terminal windows)

**Terminal 1 - User Service:**
```bash
cd user_service
source venv/bin/activate
opentelemetry-instrument python manage.py runserver 8000 --noreload

```

**Terminal 2 - Product Service:**
```bash
cd product_service
source venv/bin/activate
opentelemetry-instrument python manage.py runserver 8001 --noreload
```

**Terminal 3 - Order Service:**
```bash
cd order_service
source venv/bin/activate
opentelemetry-instrument python manage.py runserver 8002 --noreload
```

### 3. Load Dummy Data
python create_sample_data.py

### 4. Hit sample api
python simple_api_demo


## API Endpoints

### User Service (http://localhost:8000)

- `GET/POST /users/` - List/Create users
- `GET/PUT/DELETE /users/{id}/` - User details
- `GET/PUT /profiles/{id}/` - User profile details
- `GET /api/user/{user_id}/` - Get user by ID (for other services)
- `POST /api/verify/` - Verify user credentials (for other services)

### Product Service (http://localhost:8001)

- `GET/POST /categories/` - List/Create categories
- `GET/PUT/DELETE /categories/{id}/` - Category details
- `GET/POST /products/` - List/Create products
  - Query params: `?category=electronics&search=phone`
- `GET/PUT/DELETE /products/{id}/` - Product details
- `GET /api/product/{product_id}/` - Get product by ID (for other services)
- `POST /api/check-stock/` - Check product stock (for other services)
- `POST /api/update-stock/` - Update product stock (for other services)

### Order Service (http://localhost:8002)

- `GET/POST /orders/` - List/Create orders
  - Query params: `?user_id=1`
- `GET/PUT/DELETE /orders/{id}/` - Order details
- `POST /orders/{id}/cancel/` - Cancel order

## Sample Data Creation

### 1. Create Users (User Service)
```bash
curl -X POST http://localhost:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "password": "password123",
    "phone": "1234567890",
    "address": "123 Main St, City"
  }'
```

### 2. Create Categories and Products (Product Service)
```bash
# Create category
curl -X POST http://localhost:8001/categories/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Electronics",
    "description": "Electronic gadgets and devices"
  }'

# Create product
curl -X POST http://localhost:8001/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "iPhone 15",
    "description": "Latest iPhone model",
    "price": "999.99",
    "category_id": 1,
    "stock_quantity": 50
  }'
```

### 3. Create Order (Order Service)
```bash
curl -X POST http://localhost:8002/orders/ \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "shipping_address": "123 Main St, City",
    "items": [
      {
        "product_id": 1,
        "quantity": 2,
        "price": "999.99"
      }
    ]
  }'
```

## Inter-Service Communication

The services communicate via HTTP/JSON:

1. **Order Service → User Service**: Validates users exist before creating orders
2. **Order Service → Product Service**: 
   - Checks product availability and stock
   - Updates inventory when orders are placed/cancelled
   - Fetches product details for order display

3. **All services** expose internal APIs (prefixed with `/api/`) for inter-service communication

## Features Demonstrated

- **Microservices Architecture**: Each service is independent with its own database
- **Inter-Service Communication**: HTTP-based communication between services
- **Data Consistency**: Transactional operations when creating/cancelling orders
- **Service Integration**: Orders fetch real-time data from User and Product services
- **Error Handling**: Proper error responses when services are unavailable
- **CORS Configuration**: Services can communicate with each other
- **RESTful APIs**: Standard REST endpoints for all operations
