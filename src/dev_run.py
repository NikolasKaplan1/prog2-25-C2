from app import app, register_blueprints, init_db
import os

if __name__ == "__main__":
    # Configuraciones desde variables de entorno
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    host = os.getenv("HOST", "0.0.0.0")

    # Registra rutas y blueprints
    register_blueprints()

    # Inicializa la base de datos
    init_db()

    # Inicializamos el servidor
    app.run(host=host, port=port, debug=debug)
