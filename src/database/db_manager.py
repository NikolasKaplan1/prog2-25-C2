"""
Gestor de base de datos SQLite para el simulador de bolsa.
"""

import sqlite3
from pathlib import Path
from contextlib import contextmanager
from typing import Iterator

DB_PATH = Path(__file__).with_name("simulador.db")   # src/database/simulador.db
SCHEMA   = Path(__file__).with_name("schema.sql")


def init_db(seed: bool = True) -> None:
    """Crea las tablas y carga datos de ejemplo si `seed` es True."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(SCHEMA.read_text(encoding="utf-8"))

        if seed:
            conn.execute("""INSERT OR IGNORE INTO mercados
                            (nombre, moneda, ubicacion)
                            VALUES ('NYSE', 'USD', 'Nueva York')""")
            conn.execute("""INSERT OR IGNORE INTO acciones
                            (simbolo, nombre, sector, precio_actual, mercado_id)
                            VALUES ('AAPL', 'Apple Inc.', 'Tecnología', 180,
                                   (SELECT id FROM mercados WHERE nombre='NYSE'))""")
            conn.commit()


@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
    """Context manager que abre y cierra conexión con row_factory tipo dict."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
    finally:
        conn.close()