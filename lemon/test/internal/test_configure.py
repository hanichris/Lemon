import unittest
from typing import cast

from src.internal.setup import lemon_squeezy_setup, Config
from src.internal.utils import get_kv, CONFIG_KEY, Error

def err(error: Error):
    raise RuntimeError(f"Lemon Squeezy API error: {error.message}")

class TestConfiguration(unittest.TestCase):
    def setUp(self) -> None:
        self.APIKEY = "234974235"
        self.err_fun = err

    def test_lemon_squeezy_setup(self):
        config = lemon_squeezy_setup(Config(
            api_key=self.APIKEY,
            on_error=self.err_fun
        ))
        self.assertDictEqual(config.model_dump(), cast(dict, get_kv(CONFIG_KEY)))
        self.assertEqual(config.api_key, self.APIKEY)
        self.assertTrue(callable(config.on_error))