# main.py
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel, EmailStr, constr
from typing import Optional, List
import datetime
from fastapi.security import OAuth2PasswordBearer
import jwt
from passlib.context import CryptContext

# Database Configuration
SQLALCHEMY_DATABASE_URL = "mysql://user:password@localhost/coffee_shop_db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Database Models
class User(Base):
    __tablename__ = "users"
    email = Column(String(100), primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    gender = Column(String(10))
    mobile_number = Column(String(15))
    password = Column(String(100))
    image_url = Column(String(200))
    is_verified = Column(Boolean, default=False)

class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True, index=True)
    state = Column(String(50))
    city_id = Column(Integer, ForeignKey("cities.id"))
    postal_code = Column(String(10))
    user_email = Column(String(100), ForeignKey("users.email"))

class City(Base):
    __tablename__ = "cities"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    district_id = Column(Integer, ForeignKey("districts.id"))

class District(Base):
    __tablename__ = "districts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    province_id = Column(Integer, ForeignKey("provinces.id"))

class Province(Base):
    __tablename__ = "provinces"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))

class Admin(Base):
    __tablename__ = "admins"
    email = Column(String(100), primary_key=True)
    mobile_number = Column(String(15))
    password = Column(String(100))
    image_url = Column(String(200))

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    employee_role_id = Column(Integer, ForeignKey("employee_roles.id"))
    image_url = Column(String(200))
    password = Column(String(100))
    status = Column(Boolean, default=True)

class EmployeeRole(Base):
    __tablename__ = "employee_roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    description = Column(String(500))
    price = Column(Float)
    category_id = Column(Integer)
    ratings = Column(Float)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class ProductImage(Base):
    __tablename__ = "product_images"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    image_url = Column(String(200))

class CustomerReview(Base):
    __tablename__ = "customer_reviews"
    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String(100), ForeignKey("users.email"))
    message = Column(String(500))
    rating = Column(Float)
    product_id = Column(Integer, ForeignKey("products.id"))

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String(100), ForeignKey("users.email"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    total_price = Column(Float)
    status = Column(String(20))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

# Pydantic Models for Request/Response
class UserCreate(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    gender: str
    mobile_number: str
    password: str
    image_url: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# FastAPI App
app = FastAPI(title="Coffee Shop API")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# User Routes
@app.post("/users/signup")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = pwd_context.hash(user.password)
    db_user = User(**user.dict(exclude={'password'}), password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User created successfully"}

@app.post("/users/login")
async def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = jwt.encode({"email": user.email}, "secret_key", algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}

# More routes for other functionalities can be added here...

# Create tables
Base.metadata.create_all(bind=engine)
