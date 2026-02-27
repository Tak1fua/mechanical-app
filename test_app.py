import unittest
import os
from app import app, db
from models import Company, Vehicle, ServiceHistory
from datetime import date

class MechanicShopTestCase(unittest.TestCase):
    def setUp(self):
        """Set up a temporary database before each test"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Clean up the database after each test"""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_company_creation(self):
        """Test creating a company"""
        with app.app_context():
            # Add via model directly for simplicity in testing logic core
            c = Company(name="Transportes S.A.", tax_id="12345678-9", contact_info="contacto@transporte.com")
            db.session.add(c)
            db.session.commit()
            
            company = Company.query.first()
            self.assertIsNotNone(company)
            self.assertEqual(company.name, "Transportes S.A.")

    def test_vehicle_creation(self):
        """Test creating a vehicle linked to a company"""
        with app.app_context():
            c = Company(name="Transportes S.A.", tax_id="12345678-9")
            db.session.add(c)
            db.session.commit()

            v = Vehicle(plate="ABC-123", make="Toyota", model="Hilux", year=2020, company_id=c.id)
            db.session.add(v)
            db.session.commit()

            vehicle = Vehicle.query.first()
            self.assertIsNotNone(vehicle)
            self.assertEqual(vehicle.plate, "ABC-123")
            self.assertEqual(vehicle.company.name, "Transportes S.A.")

    def test_service_history(self):
        """Test adding a service history record"""
        with app.app_context():
            c = Company(name="Logistica Global", tax_id="98765432-1")
            db.session.add(c)
            db.session.commit()

            v = Vehicle(plate="XYZ-987", make="Ford", model="Ranger", year=2019, company_id=c.id)
            db.session.add(v)
            db.session.commit()

            s = ServiceHistory(vehicle_id=v.id, date=date(2023, 10, 1), description="Cambio de aceite", cost=50.0)
            db.session.add(s)
            db.session.commit()

            history = ServiceHistory.query.first()
            self.assertIsNotNone(history)
            self.assertEqual(history.description, "Cambio de aceite")
            self.assertEqual(history.vehicle.plate, "XYZ-987")

    def test_index_route(self):
        """Test the index route returns 200"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Panel de Control', response.data)

    def test_post_company_route(self):
        """Test adding a company via POST request"""
        response = self.app.post('/companies', data=dict(
            name="Empresa Test",
            tax_id="111-222",
            contact_info="Test Info"
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Empresa Test', response.data)

if __name__ == '__main__':
    unittest.main()
