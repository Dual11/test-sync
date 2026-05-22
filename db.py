import os
import psycopg2
from psycopg2.extras import RealDictCursor

class DB:
    def __init__(self):
        self.dsn = os.getenv("DATABASE_URL")
        if not self.dsn:
            raise ValueError("DATABASE_URL no está configurada en Dokploy")

    def connect(self):
        return psycopg2.connect(self.dsn, cursor_factory=RealDictCursor)