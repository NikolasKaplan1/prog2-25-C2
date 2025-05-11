from src.database.db_manager import init_db

if __name__ == "__main__":
    init_db(seed=True)   # o False si no quieres datos demo
    print("✔ Base de datos creada / reiniciada")
