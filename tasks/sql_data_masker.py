import re
from typing import List, Tuple

class SQLDataMasker:
    """
    A class for masking sensitive data in SQL queries. This includes detecting and anonymizing
    sensitive information such as email addresses, phone numbers, and credit card numbers.
    """

    # Define regex patterns for sensitive data
    SENSITIVE_PATTERNS = {
        "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "phone": r"(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}",
        "credit_card": r"\b(?:\d[ -]*?){13,16}\b",
        "ssn": r"\b\d{3}-\d{2}-\d{4}\b"
    }

    MASKING_REPLACEMENTS = {
        "email": "[masked-email]",
        "phone": "[masked-phone]",
        "credit_card": "[masked-credit-card]",
        "ssn": "[masked-ssn]"
    }

    def __init__(self):
        """
        Initializes the SQLDataMasker class.
        """
        pass

    def mask_sensitive_data(self, sql_query: str) -> str:
        """
        Masks sensitive data in the given SQL query.

        :param sql_query: The SQL query string to be masked.
        :return: The SQL query with sensitive data masked.
        """
        masked_query = sql_query
        for data_type, pattern in self.SENSITIVE_PATTERNS.items():
            masked_query = re.sub(pattern, self.MASKING_REPLACEMENTS[data_type], masked_query)
        return masked_query

    def detect_sensitive_data(self, sql_query: str) -> List[Tuple[str, str]]:
        """
        Detects sensitive data in the given SQL query.

        :param sql_query: The SQL query string to be analyzed.
        :return: A list of tuples containing the data type and the detected sensitive data.
        """
        detected_data = []
        for data_type, pattern in self.SENSITIVE_PATTERNS.items():
            matches = re.findall(pattern, sql_query)
            for match in matches:
                detected_data.append((data_type, match))
        return detected_data


# Example usage
if __name__ == "__main__":
    masker = SQLDataMasker()
    sample_query = """
        SELECT * FROM users
        WHERE email = 'user@example.com'
        AND phone = '+1-800-555-1234'
        AND credit_card = '4111 1111 1111 1111'
        AND ssn = '123-45-6789';
    """

    print("Original Query:")
    print(sample_query)

    masked_query = masker.mask_sensitive_data(sample_query)
    print("\nMasked Query:")
    print(masked_query)

    detected = masker.detect_sensitive_data(sample_query)
    print("\nDetected Sensitive Data:")
    for data_type, value in detected:
        print(f"{data_type}: {value}")