import unittest
import os
import json
from api.app import app
from api.config import app_config

class ApiTest(unittest.TestCase):
    """Test Case for API endpoint"""

    def setUp(self):
        """Initialize variable for testing"""

        self.app = app
        self.app.config.from_object(app_config['testing'])
        self.client = self.app.test_client
        self.company_name = 'BEN TRE AQUAPRODUCT IMPORT AND EXPORT JSC'

    def test_get_all(self):
        """Test to fetch all companies"""
        res = self.client().get('/api/companies')
        self.assertEqual(res.status_code, 200)
        self.assertIn('company_name', str(res.data))

    def test_get_by_company(self):
        """Test to fetch company by name"""
        param = self.company_name
        res = self.client().get('/api/companies?company_name={}'.format(param))
        self.assertEqual(res.status_code, 200)
        self.assertIn(param, str(res.data))

    def test_get_by_industry(self):
        """Test to fetch company by industry"""
        param = 'food processing'
        res = self.client().get('/api/companies?industry={}'.format(param))
        self.assertEqual(res.status_code, 200)
        self.assertIn(param, str(res.data).lower())

    def test_get_by_revenue(self):
        """Test to fetch company by revenue"""
        param = '81000000000'
        res = self.client().get('/api/companies?revenue_gte={}'.format(param))
        self.assertEqual(res.status_code, 200)
        self.assertIn(self.company_name.lower(), str(res.data).lower())

    def test_error(self):
        """Test to handle bad query parameters"""
        res = self.client().get('/api/companies?error=err')
        self.assertEqual(res.status_code, 400)

if __name__ == "__main__":
    unittest.main()