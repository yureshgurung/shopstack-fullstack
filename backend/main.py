from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional, List
from jose import JWTError, jwt
from dotenv import load_dotenv
import bcrypt
import os

import models, schemas, crud
from database import SessionLocal, engine


import logging
import sys

# ============================================
# LOGGING SETUP (12-Factor: stdout only)
# ============================================

# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s [%(levelname)s] %(message)s",
#     stream=sys.stdout,   # log to console/stdout
#     force=True
# )

# logger = logging.getLogger(__name__)
import logging
import sys
from pythonjsonlogger import jsonlogger

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

# remove old handlers (VERY IMPORTANT)
logger.handlers.clear()

handler = logging.StreamHandler(sys.stdout)

formatter = jsonlogger.JsonFormatter(
    "%(asctime)s %(levelname)s %(name)s %(message)s"
)

handler.setFormatter(formatter)

logger.addHandler(handler)

logger.propagate = False

# ── Create all tables in MySQL ─────────────────────────────────────────────────
models.Base.metadata.create_all(bind=engine)

# ── Load environment variables ─────────────────────────────────────────────────
load_dotenv()

SECRET_KEY                = os.getenv("SECRET_KEY")
ALGORITHM                 = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# ── App setup ──────────────────────────────────────────────────────────────────
app = FastAPI(title="Product Manager API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# ── DB dependency ──────────────────────────────────────────────────────────────
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ── Password helpers ───────────────────────────────────────────────────────────
def verify_password(plain: str, hashed: str) -> bool:
    pw = plain.encode("utf-8")[:72]
    return bcrypt.checkpw(pw, hashed.encode("utf-8"))


def hash_password(password: str) -> str:
    pw = password.encode("utf-8")[:72]
    return bcrypt.hashpw(pw, bcrypt.gensalt()).decode("utf-8")


# ── JWT helpers ────────────────────────────────────────────────────────────────
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = crud.get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    return user


# ── Auth routes ────────────────────────────────────────────────────────────────
# @app.post("/register", response_model=schemas.UserOut, status_code=201)
# def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     if crud.get_user_by_username(db, user.username):
#         raise HTTPException(status_code=400, detail="Username already registered")
#     hashed = hash_password(user.password)
#     return crud.create_user(db, user, hashed)
@app.post("/register", response_model=schemas.UserOut, status_code=201)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):

    logger.info(f"Register attempt: {user.username}")

    if crud.get_user_by_username(db, user.username):
        logger.warning(f"Username already exists: {user.username}")
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed = hash_password(user.password)

    logger.info(f"User created successfully: {user.username}")

    return crud.create_user(db, user, hashed)


# @app.post("/token", response_model=schemas.Token)
# def login(
#     form_data: OAuth2PasswordRequestForm = Depends(),
#     db: Session = Depends(get_db),
# ):
#     user = crud.get_user_by_username(db, form_data.username)
#     if not user or not verify_password(form_data.password, user.hashed_password):
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#     token = create_access_token(
#         data={"sub": user.username},
#         expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
#     )
#     return {"access_token": token, "token_type": "bearer"}
@app.post("/token", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):

    logger.info(f"Login attempt: {form_data.username}")

    user = crud.get_user_by_username(db, form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password):
        logger.warning(f"Failed login: {form_data.username}")
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    logger.info(f"Login successful: {form_data.username}")

    token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return {"access_token": token, "token_type": "bearer"}


@app.get("/me", response_model=schemas.UserOut)
def me(current_user=Depends(get_current_user)):
    return current_user


# ── Product routes ─────────────────────────────────────────────────────────────
@app.get("/products", response_model=List[schemas.ProductOut])
def list_products(db: Session = Depends(get_db)):
    """Public – anyone can browse products."""
    return crud.get_all_products(db)


@app.get("/products/{product_id}", response_model=schemas.ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Public – anyone can view a single product."""
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.post("/products", response_model=schemas.ProductOut, status_code=201)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Auth required – create a product."""
    return crud.create_product(db, product, owner_id=current_user.id)


@app.put("/products/{product_id}", response_model=schemas.ProductOut)
def update_product(
    product_id: int,
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Auth required – update own product."""
    db_product = crud.get_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    if db_product.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your product")
    return crud.update_product(db, db_product, product)


@app.delete("/products/{product_id}", status_code=204)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Auth required – delete own product."""
    db_product = crud.get_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    if db_product.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your product")
    crud.delete_product(db, db_product)