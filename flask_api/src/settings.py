import os

from pydantic import BaseSettings


class AuthSettings(BaseSettings):
    db_name: str = os.getenv('DB_NAME', 'price')
    pg_user: str = os.getenv('POSTGRES_USER', 'price')
    pg_pass: str = os.getenv('POSTGRES_PASSWORD', 'price')
    db_host: str = os.getenv('POSTGRES_HOST', '127.0.0.1')
    db_port: int = int(os.getenv('DB_PORT', 5432))
    redis_host: str = os.getenv('REDIS_HOST', '127.0.0.1')
    redis_port: int = int(os.getenv('REDIS_PORT', 6379))
    api_port: int = int(os.getenv('API_PORT', 5000))


config = AuthSettings()
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = (
    f'postgresql://{config.pg_user}:' f'{config.pg_pass}@{config.db_host}:{config.db_port}/{config.db_name}'
)
SWAGGER = {'title': 'OA3 Callbacks', 'openapi': '3.0.2', 'specs_route': '/swagger/'}
