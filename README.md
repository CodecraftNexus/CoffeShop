# Coffee Shop API - FastAPI & MySQL

## විශේෂාංග (Features)
- ✨ FastAPI භාවිතා කර සාදන ලද RESTful API
- 📦 MySQL Database සම්බන්ධතාවය
- 🔄 CRUD Operations සඳහා Endpoints
- 📝 Swagger UI Documentation
- ⚡ High Performance & Async Support

## තාක්ෂණික අවශ්‍යතා (Technical Requirements)
- Python 3.8+
- MySQL 5.7+
- pip (Python Package Manager)

## ස්ථාපනය (Installation)

### 1. Repository එක Clone කරගන්න
```bash
git clone <your-repository-url>
cd coffee-shop-api
```

### 2. Python Virtual Environment එකක් සාදාගන්න
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Dependencies Install කරගන්න
```bash
pip install -r requirements.txt
```

### 4. MySQL Database එක සකසා ගන්න
```sql
CREATE DATABASE coffee_shop_db;
USE coffee_shop_db;
```

### 5. Environment Variables සකසා ගන්න
`.env` ගොනුවක් සාදා පහත variables සකසන්න:
```env
DB_HOST=localhost
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=coffee_shop_db
```

## API එක Run කිරීම (Running the API)

### Development Server
```bash
uvicorn main:app --reload
```
API එක http://localhost:8000 මත run වනු ඇත.

### Production Server
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Endpoints Test කිරීම (Testing API Endpoints)

### 1. Swagger UI භාවිතය
- Browser එකෙන් http://localhost:8000/docs වෙත යන්න
- එහි ඇති UI එක භාවිතා කර endpoints test කරන්න

### 2. cURL Commands භාවිතය

#### Products
```bash
# Create Product
curl -X 'POST' \
  'http://localhost:8000/products/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Cappuccino",
  "description": "Italian coffee drink",
  "price": 350.00,
  "category": "Coffee",
  "is_available": true
}'

# Get All Products
curl -X 'GET' \
  'http://localhost:8000/products/' \
  -H 'accept: application/json'

# Get Single Product
curl -X 'GET' \
  'http://localhost:8000/products/1' \
  -H 'accept: application/json'
```

#### Orders
```bash
# Create Order
curl -X 'POST' \
  'http://localhost:8000/orders/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "customer_name": "John Doe",
  "customer_email": "john@example.com",
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    }
  ]
}'

# Get All Orders
curl -X 'GET' \
  'http://localhost:8000/orders/' \
  -H 'accept: application/json'
```

### 3. Python Requests භාවිතය
```python
import requests

# Configuration
BASE_URL = "http://localhost:8000"

# Test Products API
def test_products():
    # Create product
    product_data = {
        "name": "Espresso",
        "description": "Strong coffee shot",
        "price": 250.00,
        "category": "Coffee",
        "is_available": True
    }
    
    response = requests.post(f"{BASE_URL}/products/", json=product_data)
    print("Create Product:", response.json())
    
    # Get all products
    response = requests.get(f"{BASE_URL}/products/")
    print("All Products:", response.json())

# Test Orders API
def test_orders():
    # Create order
    order_data = {
        "customer_name": "Jane Doe",
        "customer_email": "jane@example.com",
        "items": [
            {
                "product_id": 1,
                "quantity": 2
            }
        ]
    }
    
    response = requests.post(f"{BASE_URL}/orders/", json=order_data)
    print("Create Order:", response.json())
    
    # Get all orders
    response = requests.get(f"{BASE_URL}/orders/")
    print("All Orders:", response.json())

if __name__ == "__main__":
    test_products()
    test_orders()
```

## දත්ත ආකෘති (Data Models)

### Product Model
```python
{
    "id": int,
    "name": str,
    "description": str,
    "price": float,
    "category": str,
    "is_available": bool,
    "created_at": datetime,
    "updated_at": datetime
}
```

### Order Model
```python
{
    "id": int,
    "customer_name": str,
    "customer_email": str,
    "total_amount": float,
    "status": str,
    "created_at": datetime,
    "items": [
        {
            "product_id": int,
            "quantity": int
        }
    ]
}
```

## Error Handling

API එක පහත error codes භාවිතා කරයි:
- 200: Success
- 201: Created
- 400: Bad Request
- 404: Not Found
- 500: Internal Server Error

## Development Tips

1. **Database Migrations:**
```bash
# Create migration
alembic revision --autogenerate -m "description"

# Run migration
alembic upgrade head
```

2. **Testing:**
```bash
# Run tests
pytest tests/
```

3. **Code Formatting:**
```bash
# Format code
black .

# Check imports
isort .
```

## Security Considerations

1. CORS සක්‍රීය කිරීම:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

2. Rate Limiting සක්‍රීය කිරීම:
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
```

## Deployment

### Docker භාවිතය
```dockerfile
FROM python:3.9

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Docker image එක build කිරීම සහ run කිරීම:
```bash
docker build -t coffee-shop-api .
docker run -p 8000:8000 coffee-shop-api
```

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [MySQL Documentation](https://dev.mysql.com/doc/)

## Support

ගැටලු හෝ යෝජනා ඇත්නම් GitHub Issues හරහා දැනුම් දෙන්න.
