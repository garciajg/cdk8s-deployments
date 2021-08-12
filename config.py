from dotenv import load_dotenv
import os

load_dotenv()

PG_ADMIN_EMAIL = os.getenv("PG_ADMIN_EMAIL", "my@mail.com")
PG_ADMIN_PASSWORD = os.getenv("PG_ADMIN_PASSWORD", "absecret123")
PG_ADMIN_PORT = int(os.getenv("PG_ADMIN_PORT", "8000"))
HELLO_KUB_PORT = int(os.getenv("HELLO_KUB_PORT", "8080"))