import unittest
from main import app, db, Inversor

class TestInversorEndpoints(unittest.TestCase):

    def setUp(self):
        # Configurar app en modo testing
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        self.client = app.test_client()

        # Crear base de datos temporal en memoria
        with app.app_context():
            db.create_all()

    def tearDown(self):
        # Eliminar base de datos después de cada test
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def seed_db(self):
        with app.app_context():
            inversores = [
                Inversor(nombre="Alice", email="alice@example.com", capital=100.0),
                Inversor(nombre="Bob", email="bob@example.com", capital=100.0),
                Inversor(nombre="Charlie", email="charlie@example.com", capital=100.0),
            ]
            db.session.add_all(inversores)
            db.session.commit()

    def test_get_inversores_empty(self):
        response = self.client.get("/inversores")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])

    def test_get_inversores(self):
        self.seed_db()
        response = self.client.get("/inversores")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0], {"id": 1, "nombre": "Alice", "email": "alice@example.com", "capital": 100.0})
        self.assertEqual(data[1], {"id": 2, "nombre": "Bob", "email": "bob@example.com", "capital": 100.0})
        self.assertEqual(data[2], {"id": 3, "nombre": "Charlie", "email": "charlie@example.com", "capital": 100.0})

    def test_get_inversor(self):
        self.seed_db()
        response = self.client.get("/inversores/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"id": 1, "nombre": "Alice", "email": "alice@example.com", "capital": 100.0})

    def test_get_inversor_not_found(self):
        self.seed_db()
        response = self.client.get("/inversores/999")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {'message': 'Inversor no encontrado'})

if __name__ == '__main__':
    unittest.main()
