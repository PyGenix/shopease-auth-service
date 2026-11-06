
import os
from dotenv import load_dotenv
from sqlalchemy.engine import URL

load_dotenv()


class Settings:
    APP_NAME = os.getenv(
        "APP_NAME", "ShopEase Authentication Service"
    )
    APP_ENV = os.getenv("APP_ENV", "development")
    APP_PORT = int(os.getenv("APP_PORT", "8002"))

    DB_HOST = os.getenv("DB_HOST", "mysql")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))
    DB_NAME = os.getenv("DB_NAME", "shopease_auth_db")
    DB_USER = os.getenv("DB_USER", "auth_user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    )

    DEFAULT_USER_ROLE = os.getenv(
        "DEFAULT_USER_ROLE", "customer"
    )

    @property
    def DATABASE_URL(self):
        return URL.create(
            drivername="mysql+pymysql",
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.DB_NAME,
            query={"charset": "utf8mb4"},
        )


settings = Settings()

if len(settings.JWT_SECRET_KEY) < 32:
    raise RuntimeError(
        "JWT_SECRET_KEY must be configured with at least 32 characters in .env"
    )
