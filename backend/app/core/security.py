from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
import hashlib

from app.core.config import settings

# Simplified password context to avoid bcrypt compatibility issues
try:
    pwd_context = CryptContext(
        schemes=["bcrypt"],
        deprecated="auto",
        bcrypt__rounds=12,
        bcrypt__ident="2b"
    )
    BCRYPT_AVAILABLE = True
except Exception as e:
    print(f"Bcrypt initialization failed: {e}")
    # Fallback to PBKDF2 if bcrypt fails
    pwd_context = CryptContext(
        schemes=["pbkdf2_sha256"],
        deprecated="auto"
    )
    BCRYPT_AVAILABLE = False

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    Supports both bcrypt and fallback hashing methods.
    """
    try:
        # Handle bcrypt's 72-byte limit by using SHA-256 pre-hashing for long passwords
        if BCRYPT_AVAILABLE and len(plain_password.encode('utf-8')) > 72:
            plain_password = hashlib.sha256(plain_password.encode('utf-8')).hexdigest()
        
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        print(f"Password verification error: {e}")
        # Try fallback verification for legacy hashes
        try:
            # Check if it's a simple SHA-256 hash
            plain_hash = hashlib.sha256(plain_password.encode('utf-8')).hexdigest()
            return plain_hash == hashed_password
        except:
            return False

def hash_password(password: str) -> str:
    """
    Hash a password using the available method (bcrypt or fallback).
    """
    try:
        # Handle bcrypt's 72-byte limit by using SHA-256 pre-hashing for long passwords
        if BCRYPT_AVAILABLE and len(password.encode('utf-8')) > 72:
            password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        
        return pwd_context.hash(password)
    except Exception as e:
        print(f"Password hashing error: {e}")
        # Fallback to SHA-256 with salt
        import secrets
        salt = secrets.token_hex(16)
        password_with_salt = password + salt
        hashed = hashlib.sha256(password_with_salt.encode('utf-8')).hexdigest()
        return f"sha256${salt}${hashed}"

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt

