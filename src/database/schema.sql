PRAGMA foreign_keys = ON;

-- 1. Usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre              TEXT    NOT NULL,
    email               TEXT    NOT NULL UNIQUE,
    password_hash       TEXT    NOT NULL,
    perfil              TEXT    NOT NULL CHECK (perfil IN ('conservador','agresivo')),
    capital_inicial     REAL    NOT NULL CHECK (capital_inicial >= 0),
    capital_disponible  REAL    NOT NULL CHECK (capital_disponible >= 0),
    fecha_registro      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. Mercados
CREATE TABLE IF NOT EXISTS mercados (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre    TEXT    NOT NULL UNIQUE,
    moneda    TEXT    NOT NULL,
    ubicacion TEXT
);

-- 3. Acciones
CREATE TABLE IF NOT EXISTS acciones (
    simbolo              TEXT PRIMARY KEY,
    nombre               TEXT NOT NULL,
    sector               TEXT,
    precio_actual        REAL NOT NULL,
    ultima_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    mercado_id           INTEGER NOT NULL REFERENCES mercados(id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

-- 4. Historial de precios
CREATE TABLE IF NOT EXISTS historial_precios (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    simbolo TEXT    NOT NULL REFERENCES acciones(simbolo)
        ON UPDATE CASCADE ON DELETE CASCADE,
    fecha   DATETIME NOT NULL,
    precio  REAL    NOT NULL
);

-- 5. Cartera (posición viva)
CREATE TABLE IF NOT EXISTS cartera (
    usuario_id   INTEGER NOT NULL REFERENCES usuarios(id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    simbolo      TEXT    NOT NULL REFERENCES acciones(simbolo)
        ON UPDATE CASCADE ON DELETE CASCADE,
    cantidad     INTEGER NOT NULL CHECK (cantidad > 0),
    precio_medio REAL    NOT NULL CHECK (precio_medio >= 0),
    PRIMARY KEY (usuario_id, simbolo)
);

-- 6. Transacciones   ← columna 'importe' ahora es REAL normal
CREATE TABLE IF NOT EXISTS transacciones (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id      INTEGER NOT NULL REFERENCES usuarios(id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    simbolo         TEXT    NOT NULL REFERENCES acciones(simbolo)
        ON UPDATE CASCADE ON DELETE CASCADE,
    tipo            TEXT    NOT NULL CHECK (tipo IN ('compra','venta')),
    cantidad        INTEGER NOT NULL CHECK (cantidad > 0),
    precio_unitario REAL    NOT NULL CHECK (precio_unitario >= 0),
    importe         REAL    NOT NULL,               -- ← calculado en la app
    fecha           DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Índices
CREATE INDEX IF NOT EXISTS idx_hist_precio_symbol_date
          ON historial_precios(simbolo, fecha DESC);
CREATE INDEX IF NOT EXISTS idx_trans_user_date
          ON transacciones(usuario_id, fecha DESC);