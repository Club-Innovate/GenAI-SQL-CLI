import unittest
from tasks.sql_data_masker import SQLDataMasker

class TestSQLDataMasker(unittest.TestCase):
    def setUp(self):
        self.masker = SQLDataMasker()

    def test_mask_email(self):
        query = "SELECT * FROM users WHERE email = 'user@example.com'"
        masked_query = self.masker.mask_sensitive_data(query)
        self.assertIn("[masked-email]", masked_query)
        self.assertNotIn("user@example.com", masked_query)

    def test_mask_phone(self):
        query = "SELECT * FROM users WHERE phone = '+1-800-555-1234'"
        masked_query = self.masker.mask_sensitive_data(query)
        self.assertIn("[masked-phone]", masked_query)
        self.assertNotIn("+1-800-555-1234", masked_query)

    def test_mask_credit_card(self):
        query = "SELECT * FROM payments WHERE card_number = '4111 1111 1111 1111'"
        masked_query = self.masker.mask_sensitive_data(query)
        self.assertIn("[masked-credit-card]", masked_query)
        self.assertNotIn("4111 1111 1111 1111", masked_query)

    def test_mask_ssn(self):
        query = "SELECT * FROM employees WHERE ssn = '123-45-6789'"
        masked_query = self.masker.mask_sensitive_data(query)
        self.assertIn("[masked-ssn]", masked_query)
        self.assertNotIn("123-45-6789", masked_query)

    def test_detect_sensitive_data(self):
        query = "SELECT * FROM users WHERE email = 'user@example.com' AND phone = '+1-800-555-1234'"
        detected = self.masker.detect_sensitive_data(query)
        self.assertEqual(len(detected), 2)
        self.assertIn(("email", "user@example.com"), detected)
        self.assertIn(("phone", "+1-800-555-1234"), detected)

    def test_no_sensitive_data(self):
        query = "SELECT * FROM orders WHERE order_id = 12345"
        masked_query = self.masker.mask_sensitive_data(query)
        self.assertEqual(query, masked_query)
        detected = self.masker.detect_sensitive_data(query)
        self.assertEqual(len(detected), 0)

if __name__ == "__main__":
    unittest.main()
