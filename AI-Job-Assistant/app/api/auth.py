
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pwdlib import PasswordHash
from jose import jwt

from app.database.database import get_connection


router = APIRouter()


# Password hashing
password_hash = PasswordHash.recommended()


# JWT configuration
SECRET_KEY = "ai-job-assistant-secret-key"
ALGORITHM = "HS256"


# Register request
class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str


# Login request
class LoginRequest(BaseModel):
    username: str
    password: str


# Register API
@router.post("/register")
def register(request: RegisterRequest):

    connection = get_connection()
    cursor = connection.cursor()

    # Check username
    cursor.execute(
        "SELECT id FROM users WHERE username = ?",
        (request.username,)
    )

    if cursor.fetchone():
        connection.close()

        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    # Check email
    cursor.execute(
        "SELECT id FROM users WHERE email = ?",
        (request.email,)
    )

    if cursor.fetchone():
        connection.close()

        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    # Hash password
    hashed_password = password_hash.hash(
        request.password
    )

    # Save user
    cursor.execute(
        """
        INSERT INTO users
        (username, email, password_hash)
        VALUES (?, ?, ?)
        """,
        (
            request.username,
            request.email,
            hashed_password
        )
    )

    connection.commit()

    user_id = cursor.lastrowid

    connection.close()

    return {
        "message": "User registered successfully",
        "user_id": user_id,
        "username": request.username,
        "email": request.email
    }


# Login API
@router.post("/login")
def login(request: LoginRequest):

    connection = get_connection()
    cursor = connection.cursor()

    # Find user
    cursor.execute(
        """
        SELECT id, username, email, password_hash
        FROM users
        WHERE username = ?
        """,
        (request.username,)
    )

    user = cursor.fetchone()

    connection.close()

    # User not found
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    user_id, username, email, stored_password = user

    # Verify password
    if not password_hash.verify(
        request.password,
        stored_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    # JWT data
    token_data = {
        "user_id": user_id,
        "username": username
    }

    # Create JWT token
    access_token = jwt.encode(
        token_data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user_id,
        "username": username
    }
