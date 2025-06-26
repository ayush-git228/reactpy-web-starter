import os
from pathlib import Path
import jwt
import json
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from passlib.hash import argon2

load_dotenv()
_secret = os.getenv("JWT_SECRET")
if _secret is None:
    print("WARNING: JWT_SECRET not set in .env file. Generating a random one for development.")
    print("         For production, please set a strong, unique JWT_SECRET.")
    SECRET = os.urandom(32).hex()
else:
    SECRET = _secret

USER_DB_PATH = Path(__file__).parent / "users.json"

def _load_users():
    if not USER_DB_PATH.exists():
        return {}
    try:
        with open(USER_DB_PATH, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {USER_DB_PATH}. Starting with empty users.")
        return {}

def _save_users(users):
    try:
        with open(USER_DB_PATH, 'w') as f:
            json.dump(users, f, indent=4)
    except IOError as e:
        print(f"Error: Could not save users to {USER_DB_PATH}: {e}")

def register_user(username: str, password: str) -> bool:
    users = _load_users()
    if username in users:
        return False
    hashed_password = argon2.hash(password)
    users[username] = {"password": hashed_password}
    _save_users(users)
    return True

def verify_password(username: str, password: str) -> bool:
    users = _load_users()
    user_data = users.get(username)
    if user_data:
        try:
            return argon2.verify(password, user_data["password"])
        except Exception:
            return False
    return False

def generate_token(username: str) -> str:
    payload = {
        "user": username,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET, algorithm="HS256")
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return token

def verify_token(token: str) -> dict | None:
    try:
        decoded = jwt.decode(token, SECRET, algorithms=["HS256"])
        return decoded
    except ExpiredSignatureError:
        return None
    except InvalidTokenError:
        return None
    except Exception as e:
        return None