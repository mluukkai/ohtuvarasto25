"""Tests for the Flask web application."""
import unittest
from app import app


class TestFlaskApp(unittest.TestCase):
    """Test cases for Flask web application."""

    def setUp(self):
        """Set up test client."""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_index_page_loads(self):
        """Test that the index page loads successfully."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Varastonhallintaj', response.data)

    def test_create_warehouse(self):
        """Test creating a new warehouse."""
        response = self.client.post('/create', data={
            'name': 'Testivarasto',
            'tilavuus': '100',
            'alku_saldo': '50'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Testivarasto', response.data)
        self.assertIn(b'luotu onnistuneesti', response.data)

    def test_create_warehouse_invalid_capacity(self):
        """Test creating warehouse with invalid capacity."""
        response = self.client.post('/create', data={
            'name': 'Testivarasto',
            'tilavuus': '0',
            'alku_saldo': '0'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'suurempi kuin 0', response.data)

    def test_create_warehouse_missing_name(self):
        """Test creating warehouse without a name."""
        response = self.client.post('/create', data={
            'name': '',
            'tilavuus': '100',
            'alku_saldo': '0'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'pakollinen', response.data)

    def test_add_to_nonexistent_warehouse(self):
        """Test adding to a non-existent warehouse."""
        response = self.client.post('/add/99999', data={
            'maara': '20'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ei l', response.data)

    def test_take_from_nonexistent_warehouse(self):
        """Test taking from a non-existent warehouse."""
        response = self.client.post('/take/99999', data={
            'maara': '20'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ei l', response.data)

    def test_delete_nonexistent_warehouse(self):
        """Test deleting a non-existent warehouse."""
        response = self.client.post('/delete/99999', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ei l', response.data)

