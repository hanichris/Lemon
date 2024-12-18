import os
import unittest

from typing import cast

from dotenv import load_dotenv
from pathlib import Path

from src.internal.request import fetch, FetchOptions
from src.internal.setup import lemon_squeezy_setup, Config
from src.internal.utils import Error

def err(error: Error):
    raise RuntimeError(f"Lemon Squeezy API error: {error.message}")

class TestFetchFunctionalisty(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
        load_dotenv(os.path.join(BASE_DIR, '.env'))

        lemon_squeezy_setup(Config(
            api_key= os.getenv("LEMONSQUEEZY_API_KEY"),
        ))

        self.store_id = os.getenv("LEMONSQUEEZY_STORE_ID")

    async def test_successful_call(self):
        response = await fetch(FetchOptions(
            path='/v1/users/me'
        ))

        self.assertEqual(response.get('status_code'), 200)
        self.assertIsNone(response.get('error'))
        self.assertTrue(response.get('data'))

    async def test_empty_api_key(self):
        lemon_squeezy_setup(Config(
            api_key= "",
        ))

        response = await fetch(FetchOptions(
            path='/v1/users/me'
        ))

        self.assertIsNone(response.get('status_code'))
        self.assertIsNone(response.get('data'))
        self.assertRegex(
            cast(str, response.get('error').name), # type: ignore
            "Lemon Squeezy API Error"
        )

    async def test_execution_of_error_handler_with_empty_api_key(self):
        lemon_squeezy_setup(Config(
            api_key= "",
            on_error=err
        ))

        with self.assertRaises(RuntimeError):
            await fetch(FetchOptions(
                path='/v1/users/me'
            ))

    async def test_wrong_api_key(self):
        lemon_squeezy_setup(Config(
            api_key= "0123456789",
        ))

        response = await fetch(FetchOptions(
            path='/v1/users/me'
        ))

        self.assertEqual(response.get('status_code'), 401)
        self.assertIsNotNone(response.get('data'))
        self.assertRegex(
            cast(str, response.get('error').name), # type: ignore
            "Lemon Squeezy API Error"
        )

    async def test_fetch_with_query_parameter(self):
        response = await fetch(FetchOptions(
            path='/v1/products',
            param={
                'filter[store_id]': self.store_id
            }
        ))

        self.assertEqual(response.get('status_code'), 200)
        self.assertIsNone(response.get('error'))
        self.assertTrue(response.get('data'))


    async def test_fetch_with_body_parameter(self):
        response = await fetch(FetchOptions(
            path="/v1/checkouts",
            method="POST",  # type: ignore
            body={
                "data": {
                    "type": "checkouts",
                    "attributes": {
                        "checkout_data": {
                            "email": "hello@example.com",
                            "name": "Luke Skywalker",
                            "custom": {
                                "user_id": "123",
                            }
                        },
                    },
                    "relationships": {
                        "store": {
                            "data": {
                                "type": "stores",
                                "id": f"{self.store_id}"
                            }
                        },
                        "variant": {
                            "data": {
                                "type": "variants",
                                "id": "437953"
                            }
                        }
                    },
                }
            }
        ))

        self.assertEqual(response.get('status_code'), 201)
        self.assertIsNone(response.get('error'))
        self.assertTrue(response.get('data'))