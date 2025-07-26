from fastapi import FastAPI,Form,HTTPException,status, Depends
from fastapi.middleware.cors import CORSMiddleware
from models import Base
from database import engine
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
import uuid

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Allow CORS for all origins, methods, and headers
# This is useful for development purposes, but consider restricting it in production

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

VALID_USERNAME = "kajal"
VALID_PASSWORD = "secret123"

@app.post("/login")
def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if user and user.password == password:
        session_token = str(uuid.uuid4())  # Generate UUID token
        return {
            "message": "Login successful!",
            "session_token": session_token
        }

    raise HTTPException(status_code=401, detail="Invalid credentials")


@app.post("/register")
def register(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    
    new_user = User(username=username, password=password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User registered successfully", "user_id": new_user.id}


@app.get("/userdetails")
def read_user_details(db: Session = Depends(get_db)):
    # query all users and returns all
    users = db.query(User).all()
    if users:
        return [{"name": user.username} for user in users]
    raise HTTPException(status_code=404, detail="User not found")
