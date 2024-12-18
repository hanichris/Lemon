import os
import unittest

from numbers import Number
from pathlib import Path
from typing import cast

from dotenv import load_dotenv

from src.internal.setup import lemon_squeezy_setup, Config
from src.products import list_products, get_product


class TestListProducts(unittest.IsolatedAsyncioTestCase):
    """Test the functionality of the `list_products` function."""
    def setUp(self) -> None:
        BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
        load_dotenv(os.path.join(BASE_DIR, '.env'))

        lemon_squeezy_setup(Config(
            api_key= os.getenv("LEMONSQUEEZY_API_KEY"),
        ))

        self.store_id = os.getenv("LEMONSQUEEZY_STORE_ID")

    async def test_list_all_products(self):
        """Tests that a paginated list of products is returned."""
        response = await list_products({
            "filter": {
                "store_id": self.store_id
            }
        })
        self.assertEqual(response.get('status_code'), 200)
        self.assertIsNone(response.get('error'))
        self.assertTrue(response.get('data'))

        data: list = response['data']['data']
        links: dict = response['data']['links']
        meta: dict =  response['data']['meta']
        self.assertTrue(meta.get('page'))
        self.assertGreater(len(data), 0)
        self.assertTrue(links)

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
        
        first, last = links['first'], links['last']
        self.assertIsInstance(first, str)
        self.assertIsInstance(last, str)

    async def test_filter_parameter(self):
        """Tests the paginated results are filtered by the stored id.

        Ensures that the returned response only contains data pertaining to the
        provided `store_id` value.
        """
        response = await list_products({
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

    async def test_include_parameter(self):
        """Test the API response when the `include` parameter is used."""
        response = await list_products({
            "include": ["variants"],
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
            next(filter(lambda x: x['type'] == 'variants', included), None)
        )

        first, last = links['first'], links['last']
        self.assertIsInstance(first, str)
        self.assertIsInstance(last, str)
    
    async def test_page_parameter(self):
        """Test the API response when the `page` parameter is used."""
        response = await list_products({
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


class TestGetProduct(unittest.IsolatedAsyncioTestCase):
    """Test the functionality of the `get_product` function."""
    def setUp(self) -> None:
        BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
        load_dotenv(os.path.join(BASE_DIR, '.env'))

        lemon_squeezy_setup(Config(
            api_key= os.getenv("LEMONSQUEEZY_API_KEY"),
        ))

        self.store_id = os.getenv("LEMONSQUEEZY_STORE_ID")
        self.product_id = os.getenv("LEMONSQUEEZY_PRODUCT_ID")
    
    async def test_retrieve_a_product(self):
        """Test to ensure the response contains the expected product id number.

        Examines the response received from the API to ensure that the product
        object has an id that matches the `product_id` sent with the request.
        """
        response = await get_product(cast(str | int, self.product_id))
        self.assertEqual(response.get('status_code'), 200)
        self.assertIsNone(response.get('error'))
        self.assertTrue(response.get('data'))

        data: dict = response['data']['data']
        links: dict = response['data']['links']

        self.assertTrue(links)
        self.assertTrue(data)
        self.assertEqual(
            links['self'],
            f"https://api.lemonsqueezy.com/v1/products/{self.product_id}"
        )

        _id = data['id']
        _type = data['type']
        relationships = data['relationships']
        attributes = data['attributes']

        self.assertEqual(_id, str(self.product_id))
        self.assertEqual(_type, "products")
        self.assertTrue(relationships)
        self.assertTrue(attributes)

        items = [
            attributes['buy_now_url'],
            attributes['created_at'],
            attributes['description'],
            attributes['from_price'],
            attributes['from_price_formatted'],
            attributes['large_thumb_url'],
            attributes['name'],
            attributes['pay_what_you_want'],
            attributes['price'],
            attributes['price_formatted'],
            attributes['slug'],
            attributes['status'],
            attributes['status_formatted'],
            attributes['store_id'],
            attributes['test_mode'],
            attributes['thumb_url'],
            attributes['to_price'],
            attributes['to_price_formatted'],
            attributes['updated_at'],
        ]
        for item in items:
            if item:
                self.assertIsInstance(item, bool | str | Number)
            
        self.assertEqual(attributes['store_id'], int(cast(str, self.store_id)))
        self.assertEqual(attributes['status'], 'published')
        self.assertEqual(len(attributes), len(items))

        store = relationships['store']
        variants = relationships['variants']

        self.assertTrue(store['links'])
        self.assertTrue(variants['links'])