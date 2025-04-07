import os
from src.database.db_manager import create_db_and_tables

def main():
    print("Directorio de trabajo:", os.getcwd())
    create_db_and_tables()
    print("Tablas creadas.")

if __name__ == "__main__":
    main()
