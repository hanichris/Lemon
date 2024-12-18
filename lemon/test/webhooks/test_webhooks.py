import os
import unittest

from numbers import Number
from pathlib import Path
from typing import cast

from dotenv import load_dotenv

from src.internal.setup import lemon_squeezy_setup, Config
from src.webhooks import (
    create_webhook,
    delete_webhook,
    get_webhook,
    list_webhooks,
    NewWebhook,
    update_webhook,
    UpdateWebhook
)

DATATYPE = "webhooks"
class TestCreateWebhook(unittest.IsolatedAsyncioTestCase):
    """Test the functionality of the `create_webhook` function."""

    def setUp(self) -> None:
        BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
        load_dotenv(os.path.join(BASE_DIR, '.env'))

        lemon_squeezy_setup(Config(
            api_key= os.getenv("LEMONSQUEEZY_API_KEY"),
        ))

        self.store_id = os.getenv("LEMONSQUEEZY_STORE_ID")

    async def test_error_response_for_missing_store_id_parameter(self):
        """Test that an error object was returned for a request with an erroneous parameter.
        """
        response = await create_webhook(
            "",
            cast(NewWebhook, {})
        )
        self.assertEqual(response.get('status_code'), 400)
        self.assertTrue(response.get('data'))
        self.assertIsNotNone(response.get('error'))
    
    async def test_error_response_for_empty_webhook_parameter(self):
        """Test that an error object was returned for the request with the missing
        webhook information.
        """
        response = await create_webhook(
            cast(str, self.store_id),
            cast(NewWebhook, {})
        )
        self.assertEqual(response.get('status_code'), 422)
        self.assertTrue(response.get('data'))
        self.assertIn('errors', cast(dict, response.get('data')))
        self.assertIsNotNone(response.get('error'))
    
    async def test_successful_creation_of_webhook_object(self):
        """Test that the newly created webhook object is returned."""
        response = await create_webhook(
            cast(str, self.store_id),
            {
                'url': "https://google.com/webhooks",
                'events': ['subscription_created', 'subscription_cancelled'],
                'secret': 'SUBSCRIPTION_SECRET'
            }
        )

        self.assertEqual(response.get('status_code'), 201)
        self.assertTrue(response.get('data'))
        self.assertIsNone(response.get('error'))

        self.assertTrue(response['data']['data'])
        self.assertTrue(response['data']['links'])
    
        data = response['data']
        _id = data['data']['id']
        _type = data['data']['type']
        attributes = data['data']['attributes']
        relationships = data['data']['relationships']

        self.assertTrue(_id)
        self.assertTrue(relationships)
        self.assertTrue(attributes)
        self.assertEqual(_type, DATATYPE)

        self.assertEqual(
            int(cast(str, self.store_id)),
            attributes['store_id']
        )
        self.assertEqual(
            "https://google.com/webhooks",
            attributes['url'],
        )
        self.assertListEqual(
            ['subscription_created', 'subscription_cancelled'],
            attributes['events']
        )

class TestUpdateWebhook(unittest.IsolatedAsyncioTestCase):
    """Test the functionality of the `update_webhook` function."""

    def setUp(self) -> None:
        BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
        load_dotenv(os.path.join(BASE_DIR, '.env'))

        lemon_squeezy_setup(Config(
            api_key= os.getenv("LEMONSQUEEZY_API_KEY"),
        ))

        self.store_id = os.getenv("LEMONSQUEEZY_STORE_ID")
        self.webhook_id = os.getenv("LEMONSQUEEZY_WEBHOOK_ID")
    
    async def test_error_response_for_missing_store_id_parameter(self):
        """Test that an error object was returned for a request with an erroneous parameter.
        """
        response = await update_webhook(
            "",
            cast(UpdateWebhook, {})
        )
        self.assertEqual(response.get('status_code'), 405)
        self.assertTrue(response.get('data'))
        self.assertIsNotNone(response.get('error'))
    
    async def test_successfully_update_a_webhook_object(self):
        """Test should return a webhook object on a successful update operation."""
        response = await update_webhook(
            cast(str, self.webhook_id),
            {
                'url': 'https://google.com/webhooks2',
                'events': [
                    "subscription_created",
                    "subscription_cancelled",
                    "subscription_paused",
                ],
                'secret': 'SUBSCRIPTION_SECRET_2',
        })

        self.assertEqual(response.get('status_code'), 200)
        self.assertTrue(response.get('data'))
        self.assertIsNone(response.get('error'))

        self.assertTrue(response['data']['data'])
        self.assertTrue(response['data']['links'])
    
        data = response['data']
        _id = data['data']['id']
        _type = data['data']['type']
        attributes = data['data']['attributes']
        relationships = data['data']['relationships']

        self.assertTrue(_id)
        self.assertTrue(relationships)
        self.assertTrue(attributes)
        self.assertEqual(_type, DATATYPE)

        self.assertEqual(
            int(cast(str, self.store_id)),
            attributes['store_id']
        )
        self.assertEqual(
            "https://google.com/webhooks2",
            attributes['url'],
        )
        self.assertListEqual(
            [
                "subscription_created",
                "subscription_cancelled",
                "subscription_paused",
            ],
            attributes['events']
        )

class TestGetWebhook(unittest.IsolatedAsyncioTestCase):
    """Test the functionality of the `get_webhook` function"""
    def setUp(self) -> None:
        BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
        load_dotenv(os.path.join(BASE_DIR, '.env'))

        lemon_squeezy_setup(Config(
            api_key= os.getenv("LEMONSQUEEZY_API_KEY"),
        ))

        self.store_id = os.getenv("LEMONSQUEEZY_STORE_ID")
        self.webhook_id = os.getenv("LEMONSQUEEZY_WEBHOOK_ID")
    
    async def test_successfully_retrieve_a_webhook_object(self):
        """Test should return a webhook object."""
        response = await get_webhook(cast(str, self.webhook_id))
        self.assertEqual(response.get('status_code'), 200)
        self.assertTrue(response.get('data'))
        self.assertIsNone(response.get('error'))

        self.assertTrue(response['data']['data'])
        self.assertTrue(response['data']['links'])
    
        data = response['data']
        _id = data['data']['id']
        _type = data['data']['type']
        attributes = data['data']['attributes']
        relationships = data['data']['relationships']

        self.assertTrue(_id)
        self.assertTrue(relationships)
        self.assertTrue(attributes)
        self.assertEqual(_type, DATATYPE)       

        self.assertEqual(
            int(cast(str, self.store_id)),
            attributes['store_id']
        )

        self.assertEqual(
            "https://google.com/webhooks2",
            attributes['url'],
        )
        self.assertListEqual(
            [
                "subscription_created",
                "subscription_cancelled",
                "subscription_paused",
            ],
            attributes['events']
        )
    
    async def test_successfully_retrieve_webhook_object_and_related_resources(self):
        response = await get_webhook(
            cast(str, self.webhook_id),
            {
                'include': ['store']
            }
        )
        self.assertEqual(response.get('status_code'), 200)
        self.assertTrue(response.get('data'))
        self.assertIsNone(response.get('error'))

        data: dict = response['data']['data']
        links: dict = response['data']['links']
        included: list = response['data']['included']

        self.assertTrue(links)
        self.assertTrue(data)
        self.assertIsInstance(included, list)
        self.assertIsNotNone(
            next(filter(lambda x: x['type'] == 'stores', included), None)
        )


class TestListWebhooks(unittest.IsolatedAsyncioTestCase):
    """Test the functionality of the `list_webhooks` function"""
    def setUp(self) -> None:
        BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
        load_dotenv(os.path.join(BASE_DIR, '.env'))

        lemon_squeezy_setup(Config(
            api_key= os.getenv("LEMONSQUEEZY_API_KEY"),
        ))

        self.store_id = os.getenv("LEMONSQUEEZY_STORE_ID")
    
    async def test_list_all_webhooks(self):
        """Test should return a paginated list of webhooks"""
        response = await list_webhooks()

        self.assertTrue(response.get('data'))
        self.assertIsNone(response.get('error'))
        self.assertEqual(response.get('status_code'), 200)

        data: list = response['data']['data']
        links: dict = response['data']['links']
        meta: dict =  response['data']['meta']

        self.assertTrue(meta.get('page'))
        self.assertGreater(len(data), 0)
        self.assertTrue(links)

    async def test_include_parameter(self):
        """Test should return a paginated list of webhooks with the related
        resources.
        """
        response = await list_webhooks({
            "include": ["store"],
        })

        self.assertEqual(response.get('status_code'), 200)
        self.assertIsNone(response.get('error'))
        self.assertTrue(response.get('data'))

        data: list = response['data']['data']
        links: dict = response['data']['links']
        meta: dict =  response['data']['meta']
        included: list = response['data']['included']

        self.assertTrue(meta.get('page'))
        self.assertTrue(links)
        self.assertIsInstance(data, list)
        self.assertIsInstance(included, list)
        self.assertIsNotNone(
            next(filter(lambda x: x['type'] == 'stores', included), None)
        )

    async def test_filter_by_store_id(self):
        """Test should return a list of paginated webhooks filtered by
        the store id.
        """
        response = await list_webhooks({
            "filter": {
                "store_id": self.store_id
            }
        })
        self.assertEqual(response.get('status_code'), 200)
        self.assertIsNone(response.get('error'))
        self.assertTrue(response.get('data'))

        data: list = response['data']['data']
        filtered_data = [
            item for item in filter(
                lambda x: x['attributes']['store_id'] == int(
                    cast(str, self.store_id)
                ),
                data
            )
        ]
        self.assertEqual(len(data), len(filtered_data))


class TestDeleteWebhook(unittest.IsolatedAsyncioTestCase):
    """Test the functionality of `delete_webhook`."""
    def setUp(self) -> None:
        BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
        load_dotenv(os.path.join(BASE_DIR, '.env'))

        lemon_squeezy_setup(Config(
            api_key= os.getenv("LEMONSQUEEZY_API_KEY"),
        ))

        self.store_id = os.getenv("LEMONSQUEEZY_STORE_ID")
        self.webhook_id = os.getenv("LEMONSQUEEZY_WEBHOOK_ID")
    
    async def test_successful_deletion_of_webhook_object(self):
        """Test should return a 204 No content response on success."""
        response = await delete_webhook(cast(str, self.webhook_id))
        self.assertEqual(response.get('status_code'), 204)
        self.assertIsNone(response.get('data'))
        self.assertIsNone(response.get('error'))