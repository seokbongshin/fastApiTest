import os

JWT_SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
    "VlwEyVBsYt9V7zq57TejMnVUyzblYcfPQye08f7MGVA9XkHa",
)
JWT_ALGORITHM = "HS256"
