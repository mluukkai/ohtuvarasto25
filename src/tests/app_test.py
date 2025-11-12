"""Tests for Flask web application."""
import unittest
from app import app


class TestFlaskApp(unittest.TestCase):
    """Test cases for Flask application routes."""

    def setUp(self):
        """Set up test client."""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        # Clear warehouses before each test
        from app import warehouses
        warehouses.clear()

    def test_index_page(self):
        """Test that index page loads."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Warehouse Management System', response.data)

    def test_create_page(self):
        """Test that create page loads."""
        response = self.client.get('/create')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Create New Warehouse', response.data)

    def test_create_warehouse_success(self):
        """Test creating a warehouse successfully."""
        response = self.client.post('/create', data={
            'name': 'Test Warehouse',
            'capacity': '100'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Warehouse', response.data)

    def test_create_warehouse_duplicate(self):
        """Test creating a duplicate warehouse."""
        self.client.post('/create', data={
            'name': 'Test Warehouse',
            'capacity': '100'
        })
        response = self.client.post('/create', data={
            'name': 'Test Warehouse',
            'capacity': '50'
        }, follow_redirects=True)
        self.assertIn(b'already exists', response.data)

    def test_create_warehouse_invalid_capacity(self):
        """Test creating a warehouse with invalid capacity."""
        response = self.client.post('/create', data={
            'name': 'Test Warehouse',
            'capacity': '-10'
        }, follow_redirects=True)
        self.assertIn(b'must be greater than 0', response.data)

    def test_manage_warehouse(self):
        """Test managing a warehouse."""
        self.client.post('/create', data={
            'name': 'Test Warehouse',
            'capacity': '100'
        })
        response = self.client.get('/manage/Test Warehouse')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Manage Warehouse: Test Warehouse', response.data)

    def test_add_content(self):
        """Test adding content to a warehouse."""
        self.client.post('/create', data={
            'name': 'Test Warehouse',
            'capacity': '100'
        })
        response = self.client.post('/manage/Test Warehouse', data={
            'action': 'add',
            'amount': '50'
        }, follow_redirects=True)
        self.assertIn(b'Added 50', response.data)

    def test_remove_content(self):
        """Test removing content from a warehouse."""
        self.client.post('/create', data={
            'name': 'Test Warehouse',
            'capacity': '100'
        })
        self.client.post('/manage/Test Warehouse', data={
            'action': 'add',
            'amount': '50'
        })
        response = self.client.post('/manage/Test Warehouse', data={
            'action': 'remove',
            'amount': '20'
        }, follow_redirects=True)
        self.assertIn(b'Removed 20', response.data)

    def test_delete_warehouse(self):
        """Test deleting a warehouse."""
        self.client.post('/create', data={
            'name': 'Test Warehouse',
            'capacity': '100'
        })
        response = self.client.post('/delete/Test Warehouse', follow_redirects=True)
        self.assertIn(b'deleted successfully', response.data)

    def test_manage_nonexistent_warehouse(self):
        """Test managing a warehouse that doesn't exist."""
        response = self.client.get('/manage/Nonexistent', follow_redirects=True)
        self.assertIn(b'not found', response.data)
