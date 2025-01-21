# Coffee Shop Backend API

A comprehensive backend API system for a coffee shop built using FastAPI and MySQL.

## Features

### User Management
- User registration and authentication
- Email and phone number verification
- Profile management with image upload
- Secure password hashing
- JWT token-based authentication

### Location Management
- Hierarchical location system (Province -> District -> City)
- User address management
- Postal code validation
- Multiple addresses per user

### Admin System
- Secure admin authentication
- Employee management
- Role-based access control
- Employee status monitoring

### Employee Management
- Role-based employee system
- Employee profile management
- Status tracking
- Secure authentication

### Product Management
- Comprehensive product details
- Multiple product images (up to 6 per product)
- Product categorization
- Price and availability management
- Rating system

### Review and Order System
- Customer review system
- Rating management
- Order processing
- Order status tracking

## Technical Stack

- **Framework:** FastAPI
- **Database:** MySQL
- **ORM:** SQLAlchemy
- **Authentication:** JWT
- **Password Hashing:** Bcrypt
- **API Documentation:** Swagger UI / OpenAPI

## Installation

1. Clone the repository:
```bash
git clone [[repository-url]](https://github.com/CodecraftNexus/coffee-shop-api)
cd coffee-shop-api
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up MySQL database:
```bash
mysql -u root -p
CREATE DATABASE coffee_shop_db;
```

5. Update database configuration in `main.py`:
```python
SQLALCHEMY_DATABASE_URL = "mysql://user:password@localhost/coffee_shop_db"
```

## Running the Application

1. Start the server:
```bash
uvicorn main:app --reload
```

2. Access the API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### User Management
- POST `/users/signup` - Register new user
- POST `/users/login` - User login
- PUT `/users/verify-email` - Email verification
- PUT `/users/verify-phone` - Phone verification

### Location Management
- POST `/locations` - Add new location
- GET `/provinces` - List provinces
- GET `/districts/{province_id}` - List districts
- GET `/cities/{district_id}` - List cities

### Admin Management
- POST `/admin/login` - Admin login
- POST `/admin/employees` - Add new employee
- PUT `/admin/employees/{id}` - Update employee
- GET `/admin/employees` - List employees

### Product Management
- POST `/products` - Add new product
- PUT `/products/{id}` - Update product
- POST `/products/{id}/images` - Add product images
- GET `/products` - List products
- GET `/products/{id}` - Get product details

### Review System
- POST `/reviews` - Add review
- GET `/products/{id}/reviews` - Get product reviews

### Order System
- POST `/orders` - Create order
- GET `/orders/{id}` - Get order details
- PUT `/orders/{id}/status` - Update order status

## Database Schema

The database consists of the following main tables:
- users
- locations
- provinces
- districts
- cities
- admins
- employees
- employee_roles
- products
- product_images
- customer_reviews
- orders

## Security Features

- Password hashing using bcrypt
- JWT token authentication
- Email and phone verification
- Role-based access control
- Input validation
- SQL injection prevention through ORM

## Error Handling

The API implements comprehensive error handling for:
- Invalid inputs
- Authentication failures
- Database errors
- Business logic violations
- Resource not found errors

## Development Guidelines

1. Code Style
   - Follow PEP 8 guidelines
   - Use type hints
   - Document functions and classes

2. Testing
   - Write unit tests for all endpoints
   - Test database operations
   - Validate authentication flows

3. Security
   - Keep dependencies updated
   - Validate all inputs
   - Use environment variables for sensitive data

## Future Improvements

1. Add caching layer
2. Implement rate limiting
3. Add payment gateway integration
4. Implement real-time order tracking
5. Add analytics dashboard
6. Implement backup system

## Requirements

```txt
fastapi==0.68.0
uvicorn==0.15.0
sqlalchemy==1.4.23
python-jose==3.3.0
passlib==1.7.4
python-multipart==0.0.5
email-validator==1.1.3
mysql-connector-python==8.0.26
python-jose[cryptography]==3.3.0
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
