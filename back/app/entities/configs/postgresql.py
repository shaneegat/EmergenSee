import os


class Postgresql:
    DBNAME = os.getenv("DB_NAME", "Emergensee")
    USER = os.getenv("DB_USER", "emergensee")
    PASSWORD = os.getenv("DB_PASSWORD", "local-demo-only")
    HOST = os.getenv("DB_HOST", "localhost")
    PORT = int(os.getenv("DB_PORT", "5432"))
