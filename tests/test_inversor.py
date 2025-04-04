import unittest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.pool import StaticPool
from unittest.mock import AsyncMock, MagicMock, patch

from main import app
from auth import authenticator
from database import get_session, Inversor

class TestInversorEndpoints(unittest.TestCase):

    def setUp(self):
        engine = create_engine(
            "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
        )
        SQLModel.metadata.create_all(engine)
        self.session = Session(engine)
        def get_session_override():
            yield self.session
        app.dependency_overrides[get_session] = get_session_override
        
        self.mock_auth = MagicMock()
        self.mock_auth.return_value = True
        self.patcher = patch.object(authenticator, "__call__", self.mock_auth)
        self.patcher.start()

        app.lifespan = AsyncMock(return_value=None)
        self.client = TestClient(app)       
    
    def tearDown(self):
        app.dependency_overrides.clear()
        self.patcher.stop()
    
    def seed_db(self):
        with self.session as session:
            session.add_all([
                Inversor(nombre="Alice", email="alice@example.com", capital= 100.0),
                Inversor(nombre="Bob", email="bob@example.com", capital = 100.0),
                Inversor(nombre="Charlie", email="charlie@example.com", capital = 100.0)
            ])
            session.commit()

    def test_get_inversors_empty(self):
        response = self.client.get("/inversores")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertEqual(len(response.json()), 0)

    def test_get_inversors(self):
        self.seed_db()
        response = self.client.get("/inversores")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertEqual(len(response.json()), 3)
        inversor = response.json()[0]
        self.assertIsInstance(inversor, dict)
        self.assertEqual(inversor, {"id": 1, "nombre": "Alice", "email":"alice@example.com", "capital": 100.0 })
        inversor = response.json()[1]
        self.assertIsInstance(inversor, dict)
        self.assertEqual(inversor, {"id": 2, "nombre": "Bob", "email":"bob@example.com", "capital": 100.0 })
        inversor = response.json()[2]
        self.assertIsInstance(inversor, dict)
        self.assertEqual(inversor, {"id": 3, "nombre": "Charlie", "email":"charlie@example.com", "capital": 100.0 })

    def test_get_inversor(self):
        self.seed_db()
        response = self.client.get("/inversor/1")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), dict)
        self.assertEqual(response.json(), {"id": 1, "nombre": "Alice", "email": "alice@example.com", "capital": 100.0})
    
    def test_get_inversor_not_found(self):
        self.seed_db()
        response = self.client.get("/inversor/4")
        self.assertEqual(response.status_code, 404)
        self.assertIsInstance(response.json(), dict)
        self.assertEqual(response.json(), {"detail": "Inversor no encontrado"})