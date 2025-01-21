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
SQLALCHEMY_DATABASE_URL = "mysql://root:Damith2004/11/22@localhost/coffee_shop_db"
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

# Additional Pydantic models for requests/responses
class LocationBase(BaseModel):
    state: str
    city_id: int
    postal_code: str
    user_email: str

class LocationCreate(LocationBase):
    pass

class LocationResponse(LocationBase):
    id: int

class CityBase(BaseModel):
    name: str
    district_id: int

class CityCreate(CityBase):
    pass

class CityResponse(CityBase):
    id: int

class DistrictBase(BaseModel):
    name: str
    province_id: int

class DistrictCreate(DistrictBase):
    pass

class DistrictResponse(DistrictBase):
    id: int

class ProvinceBase(BaseModel):
    name: str

class ProvinceCreate(ProvinceBase):
    pass

class ProvinceResponse(ProvinceBase):
    id: int

class AdminBase(BaseModel):
    email: EmailStr
    mobile_number: str
    password: str
    image_url: Optional[str] = None

class AdminCreate(AdminBase):
    pass

class AdminResponse(BaseModel):
    email: str
    mobile_number: str
    image_url: Optional[str]

class EmployeeRoleBase(BaseModel):
    name: str

class EmployeeRoleCreate(EmployeeRoleBase):
    pass

class EmployeeRoleResponse(EmployeeRoleBase):
    id: int

class EmployeeBase(BaseModel):
    name: str
    employee_role_id: int
    password: str
    image_url: Optional[str] = None

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeResponse(BaseModel):
    id: int
    name: str
    employee_role_id: int
    image_url: Optional[str]
    status: bool

class ProductBase(BaseModel):
    title: str
    description: str
    price: float
    category_id: int
    ratings: Optional[float] = 0.0
    is_available: bool = True

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

class ProductImageBase(BaseModel):
    product_id: int
    image_url: str

class ProductImageCreate(ProductImageBase):
    pass

class ProductImageResponse(ProductImageBase):
    id: int

class CustomerReviewBase(BaseModel):
    user_email: str
    message: str
    rating: float
    product_id: int

class CustomerReviewCreate(CustomerReviewBase):
    pass

class CustomerReviewResponse(CustomerReviewBase):
    id: int

class OrderBase(BaseModel):
    user_email: str
    product_id: int
    quantity: int
    total_price: float
    status: str = "pending"

class OrderCreate(OrderBase):
    pass

class OrderResponse(OrderBase):
    id: int
    created_at: datetime.datetime

# Location endpoints
@app.post("/locations/", response_model=LocationResponse)
async def create_location(location: LocationCreate, db: Session = Depends(get_db)):
    db_location = Location(**location.dict())
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location

@app.get("/locations/", response_model=List[LocationResponse])
async def get_locations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    locations = db.query(Location).offset(skip).limit(limit).all()
    return locations

@app.get("/locations/{location_id}", response_model=LocationResponse)
async def get_location(location_id: int, db: Session = Depends(get_db)):
    location = db.query(Location).filter(Location.id == location_id).first()
    if location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return location

# City endpoints
@app.post("/cities/", response_model=CityResponse)
async def create_city(city: CityCreate, db: Session = Depends(get_db)):
    db_city = City(**city.dict())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city

@app.get("/cities/", response_model=List[CityResponse])
async def get_cities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cities = db.query(City).offset(skip).limit(limit).all()
    return cities

@app.get("/cities/{city_id}", response_model=CityResponse)
async def get_city(city_id: int, db: Session = Depends(get_db)):
    city = db.query(City).filter(City.id == city_id).first()
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city

# District endpoints
@app.post("/districts/", response_model=DistrictResponse)
async def create_district(district: DistrictCreate, db: Session = Depends(get_db)):
    db_district = District(**district.dict())
    db.add(db_district)
    db.commit()
    db.refresh(db_district)
    return db_district

@app.get("/districts/", response_model=List[DistrictResponse])
async def get_districts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    districts = db.query(District).offset(skip).limit(limit).all()
    return districts

@app.get("/districts/{district_id}", response_model=DistrictResponse)
async def get_district(district_id: int, db: Session = Depends(get_db)):
    district = db.query(District).filter(District.id == district_id).first()
    if district is None:
        raise HTTPException(status_code=404, detail="District not found")
    return district

# Province endpoints
@app.post("/provinces/", response_model=ProvinceResponse)
async def create_province(province: ProvinceCreate, db: Session = Depends(get_db)):
    db_province = Province(**province.dict())
    db.add(db_province)
    db.commit()
    db.refresh(db_province)
    return db_province

@app.get("/provinces/", response_model=List[ProvinceResponse])
async def get_provinces(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    provinces = db.query(Province).offset(skip).limit(limit).all()
    return provinces

@app.get("/provinces/{province_id}", response_model=ProvinceResponse)
async def get_province(province_id: int, db: Session = Depends(get_db)):
    province = db.query(Province).filter(Province.id == province_id).first()
    if province is None:
        raise HTTPException(status_code=404, detail="Province not found")
    return province

# Admin endpoints
@app.post("/admins/", response_model=AdminResponse)
async def create_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    db_admin = db.query(Admin).filter(Admin.email == admin.email).first()
    if db_admin:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = pwd_context.hash(admin.password)
    db_admin = Admin(**admin.dict(exclude={'password'}), password=hashed_password)
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin

@app.get("/admins/{email}", response_model=AdminResponse)
async def get_admin(email: str, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.email == email).first()
    if admin is None:
        raise HTTPException(status_code=404, detail="Admin not found")
    return admin

# Employee role endpoints
@app.post("/employee-roles/", response_model=EmployeeRoleResponse)
async def create_employee_role(role: EmployeeRoleCreate, db: Session = Depends(get_db)):
    db_role = EmployeeRole(**role.dict())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

@app.get("/employee-roles/", response_model=List[EmployeeRoleResponse])
async def get_employee_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    roles = db.query(EmployeeRole).offset(skip).limit(limit).all()
    return roles

# Employee endpoints
@app.post("/employees/", response_model=EmployeeResponse)
async def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(employee.password)
    db_employee = Employee(**employee.dict(exclude={'password'}), password=hashed_password)
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@app.get("/employees/", response_model=List[EmployeeResponse])
async def get_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    employees = db.query(Employee).offset(skip).limit(limit).all()
    return employees

@app.get("/employees/{employee_id}", response_model=EmployeeResponse)
async def get_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

# Product endpoints
@app.post("/products/", response_model=ProductResponse)
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products/", response_model=List[ProductResponse])
async def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = db.query(Product).offset(skip).limit(limit).all()
    return products

@app.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Product image endpoints
@app.post("/product-images/", response_model=ProductImageResponse)
async def create_product_image(image: ProductImageCreate, db: Session = Depends(get_db)):
    db_image = ProductImage(**image.dict())
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

@app.get("/product-images/product/{product_id}", response_model=List[ProductImageResponse])
async def get_product_images(product_id: int, db: Session = Depends(get_db)):
    images = db.query(ProductImage).filter(ProductImage.product_id == product_id).all()
    return images

# Customer review endpoints
@app.post("/reviews/", response_model=CustomerReviewResponse)
async def create_review(review: CustomerReviewCreate, db: Session = Depends(get_db)):
    db_review = CustomerReview(**review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

@app.get("/reviews/product/{product_id}", response_model=List[CustomerReviewResponse])
async def get_product_reviews(product_id: int, db: Session = Depends(get_db)):
    reviews = db.query(CustomerReview).filter(CustomerReview.product_id == product_id).all()
    return reviews

# Order endpoints
@app.post("/orders/", response_model=OrderResponse)
async def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    db_order = Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@app.get("/orders/", response_model=List[OrderResponse])
async def get_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = db.query(Order).offset(skip).limit(limit).all()
    return orders

@app.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.get("/orders/user/{user_email}", response_model=List[OrderResponse])
async def get_user_orders(user_email: str, db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.user_email == user_email).all()
    return orders



# Create tables
Base.metadata.create_all(bind=engine)
