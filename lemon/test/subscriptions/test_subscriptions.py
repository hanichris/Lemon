import os
import unittest

from numbers import Number
from pathlib import Path
from typing import cast

from dotenv import load_dotenv

from src.internal.setup import lemon_squeezy_setup, Config
from src.subscriptions import (
    cancel_subscription,
    get_subscription,
    list_subscriptions,
    update_subscription
)


class TestListSubscriptions(unittest.IsolatedAsyncioTestCase):
    """Test the functionality of the `list_subscriptions` function."""
    def setUp(self) -> None:
        BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
        load_dotenv(os.path.join(BASE_DIR, '.env'))

        lemon_squeezy_setup(Config(
            api_key= os.getenv("LEMONSQUEEZY_API_KEY"),
        ))

        self.store_id = os.getenv("LEMONSQUEEZY_STORE_ID")
    
    async def test_list_all_subscriptions(self):
        """Test should return a paginated list of subscriptions"""
        response = await list_subscriptions()

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
        """Test should return a paginated list of subscriptions with the related
        resources.
        """
        response = await list_subscriptions({
            "include": ["product"],
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
            next(filter(lambda x: x['type'] == 'products', included), None)
        )

    async def test_filter_by_store_id(self):
        """Test should return a list of paginated subscriptions filtered by
        the store id.
        """
        response = await list_subscriptions({
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
    
    async def test_filter_by_order_id(self):
        """Test should return a list of paginated subscriptions filtered by the
        order id.
        """
        order_id = cast(str, os.getenv("LEMONSQUEEZY_USER_SUB_ORDER_ID"))
        response = await list_subscriptions({
            "filter": {
                "order_id": order_id
            }
        })
        self.assertEqual(response.get('status_code'), 200)
        self.assertIsNone(response.get('error'))
        self.assertTrue(response.get('data'))

        data: list = response['data']['data']
        filtered_data = [
            item for item in filter(
                lambda x: x['attributes']['order_id'] == int(order_id), data
            )
        ]
        self.assertEqual(len(data), len(filtered_data))

    
    async def test_filter_by_product_id(self):
        """Test should return a list of paginated subscriptions filtered by the
        product id.
        """
        product_id = cast(str, os.getenv("LEMONSQUEEZY_USER_SUB_PRODUCT_ID"))
        response = await list_subscriptions({
            "filter": {
                "product_id": product_id
            }
        })
        self.assertEqual(response.get('status_code'), 200)
        self.assertIsNone(response.get('error'))
        self.assertTrue(response.get('data'))

        data: list = response['data']['data']
        filtered_data = [
            item for item in filter(
                lambda x: x['attributes']['product_id'] == int(product_id), data
            )
        ]
        self.assertEqual(len(data), len(filtered_data))
    
    async def test_filter_by_order_item_id(self):
        """Test should return a list of paginated subscriptions filtered by the
        order item id.
        """
        order_item_id = cast(str, os.getenv("LEMONSQUEEZY_USER_SUB_ORDER_ITEM_ID"))
        response = await list_subscriptions({
            "filter": {
                "order_item_id": order_item_id
            }
        })
        self.assertEqual(response.get('status_code'), 200)
        self.assertIsNone(response.get('error'))
        self.assertTrue(response.get('data'))

        data: list = response['data']['data']
        filtered_data = [
            item for item in filter(
                lambda x: x['attributes']['order_item_id'] == int(order_item_id),
                data
            )
        ]
        self.assertEqual(len(data), len(filtered_data))
    
    async def test_filter_by_variant_id(self):
        """Test should return a list of paginated subscriptions filtered by the
        variant id.
        """
        variant_id = cast(str, os.getenv("LEMONSQUEEZY_USER_SUB_ORDER_ID"))
        response = await list_subscriptions({
            "filter": {
                "variant_id": variant_id
            }
        })
        self.assertEqual(response.get('status_code'), 200)
        self.assertIsNone(response.get('error'))
        self.assertTrue(response.get('data'))

        data: list = response['data']['data']
        filtered_data = [
            item for item in filter(
                lambda x: x['attributes']['variant_id'] == int(variant_id), data
            )
        ]
        self.assertEqual(len(data), len(filtered_data))
    
    async def test_filter_by_user_email(self):
        """Test should return a list of paginated subscriptions filtered by the
        subscribed user's email.
        """
        user_email = cast(str, os.getenv("LEMONSQUEEZY_USER_EMAIL"))
        response = await list_subscriptions({
            "filter": {
                "user_email": user_email
            }
        })
        self.assertEqual(response.get('status_code'), 200)
        self.assertIsNone(response.get('error'))
        self.assertTrue(response.get('data'))

        data: list = response['data']['data']
        filtered_data = [
            item for item in filter(
                lambda x: x['attributes']['user_email'] == user_email, data
            )
        ]
        self.assertEqual(len(data), len(filtered_data))

    async def test_page_parameter(self):
        """Test the API response when the `page` parameter is used."""
        response = await list_subscriptions({
            "page": {
                "number": 1,
                "size": 5,
            }
        })
        self.assertEqual(response.get('status_code'), 200)
        self.assertIsNone(response.get('error'))
        self.assertTrue(response.get('data'))

        links: dict = response['data']['links']
        meta: dict =  response['data']['meta']
        data: list = response['data']['data']

        self.assertIsInstance(data, list)
        self.assertTrue(meta)
        self.assertTrue(links['first'])
        self.assertTrue(links['last'])

        entries = [
            meta['page']['currentPage'],
            meta['page']['from'],
            meta['page']['lastPage'],
            meta['page']['perPage'],
            meta['page']['to'],
            meta['page']['total'],
        ]
        for entry in entries:
            self.assertIsInstance(entry, Number)
        
        self.assertEqual(len(meta['page']), len(entries))
        self.assertEqual(meta['page']['currentPage'], 1)
        self.assertEqual(meta['page']['perPage'], 5)


class TestGetSubscriptions(unittest.IsolatedAsyncioTestCase):
    """Test the functionality of the `get_subscription` function."""
    def setUp(self) -> None:
        BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
        load_dotenv(os.path.join(BASE_DIR, '.env'))

        lemon_squeezy_setup(Config(
            api_key= os.getenv("LEMONSQUEEZY_API_KEY"),
        ))

        self.store_id = os.getenv("LEMONSQUEEZY_STORE_ID")
    
    async def test_not_found_retrieval_of_subscription(self):
        """Tests the api responds with a 404 error code."""
        response = await get_subscription("notrealsubscriptionid")
        self.assertEqual(response.get('status_code'), 404)
        self.assertIsNotNone(response.get('error'))
        self.assertIn('errors', cast(dict, response.get('data')))
    
    async def test_successful_retrival_of_checkout(self):
        """Tests the api responds with the wanted subscription object."""
        subscription_id = cast(
            str,
            os.getenv("LEMONSQUEEZY_USER_SUB_SUBSCRIPTION_ID")
        )
        response = await get_subscription(subscription_id)
        self.assertTrue(response.get('data'))
        self.assertIsNone(response.get('error'))
        self.assertEqual(response.get('status_code'), 200)

        id = response['data']['data']['id']
        self.assertEqual(subscription_id, id)
    
    async def test_successful_retrival_with_related_resource(self):
        subscription_id = cast(
            str,
            os.getenv("LEMONSQUEEZY_USER_SUB_SUBSCRIPTION_ID")
        )
        response = await get_subscription(
            subscription_id,
            {
                'include': ['product'],
            }
        )
        self.assertTrue(response.get('data'))
        self.assertIsNone(response.get('error'))
        self.assertEqual(response.get('status_code'), 200)

        data: dict = response['data']['data']
        links: dict = response['data']['links']
        included: list = response['data']['included']

        self.assertTrue(links)
        self.assertTrue(data)
        self.assertIsInstance(included, list)
        self.assertIsNotNone(
            next(filter(lambda x: x['type'] == 'products', included), None)
        )
