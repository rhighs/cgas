import unittest
from ..cloudygram_api_server.scripts import TtWrap

class TestWrapper(unittest.TestCase):
    def __init__(self):
        pass
         
    def test_create_client(self):
        wrapper = TlWrap(api_id="", api_hash="")
        client = wrapper.create_client() 
        self.assertIsInstance(client)

if __name__ == "__main__":
    unittest.main()
