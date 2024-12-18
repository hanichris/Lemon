import unittest

from typing import cast

from src.internal.utils import set_kv, get_kv, clear_kv

class TestKVStore(unittest.TestCase):

    def setUp(self) -> None:
        self.config = {
            "api_key": 123456
        }
        self.key = "Store"

    def test_successful_set_operation(self):
        self.assertIsNone(get_kv(self.key))
        set_kv(self.key, self.config)
        self.assertDictEqual(self.config, cast(dict, get_kv(self.key)))
    
    def test_successful_get_operation(self):
        set_kv(self.key, self.config)
        config = cast(dict, get_kv(self.key))
        self.assertEqual(config, self.config)
        self.assertEqual(config['api_key'], self.config['api_key'])
    
    def tearDown(self) -> None:
        clear_kv()