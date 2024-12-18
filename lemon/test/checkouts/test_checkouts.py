import os
import unittest

from pathlib import Path
from typing import cast
from numbers import Number

from dotenv import load_dotenv

from src.internal.setup import lemon_squeezy_setup, Config
from src.internal.utils import Error
from src.checkouts import list_checkouts, get_checkout, create_checkout, NewCheckout

async def create_test_checkout(store_id: str, variant_id: str):
    new_checkout: NewCheckout = {            
        "product_options": {            
            "name": "New Checkout Test",
            "description": "a new checkout test",
            "confirmation_title": "Thank you for your support",
            "confirmation_message": "Thank you for subscribing and have a great day",
            "confirmation_button_text": "View Order",
        },
        "checkout_data": {
            "email": "tita0x00@gmail.com",
            "name": "Lemon Squeezy Test",
            "billing_address": {                
                "country": "US",
            },
            "tax_number": "12345",
            "custom": {
                "user_id": "1234567890",
                "user_name": "Mrs.A",
            },
        },
        "expires_at": None,
        "preview": True,
        "test_mode": True,
    }
    return await create_checkout(
        store_id,
        variant_id,
        new_checkout
    )


class TestCreateCheckout(unittest.IsolatedAsyncioTestCase):
    """Test the functionality of the `create_checkout` function."""

    def setUp(self) -> None:
        BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
        load_dotenv(os.path.join(BASE_DIR, '.env'))

        lemon_squeezy_setup(Config(
            api_key= os.getenv("LEMONSQUEEZY_API_KEY"),
        ))
        self.store_id = os.getenv("LEMONSQUEEZY_STORE_ID")
        self.variant_id = os.getenv("LEMONSQUEEZY_VARIANT_ID")
    
    async def test_error_response_for_missing_parameter(self):
        """Test that an error object was returned for a request with an erroneous parameter.
        """
        response = await create_checkout(cast(str, self.store_id), "")
        self.assertEqual(response.get('status_code'), 400)
        self.assertTrue(response.get('data'))
        self.assertIsNotNone(response.get('error'))

        self.assertIn(
            "Lemon Squeezy API Error",
            cast(str, cast(Error, response.get('error')).name)
        )
    
    async def test_erroneous_creation_of_new_checkout_with_given_store_and_variant_id(self):
        """
        Tests that a 500 server error is returned when the new checkout
        information is missing from the request.
        """
        response = await create_checkout(
            cast(str, self.store_id),
            cast(str, self.variant_id),
        )
        self.assertEqual(response.get('status_code'), 500)
        self.assertFalse(response.get('data'))
        self.assertIsNotNone(response.get('error'))

    async def test_successful_creation_of_new_checkout(self):
        """
        Tests that a new checkout is created 
        """
        DATATYPE="checkouts"
        new_checkout: NewCheckout = {            
            "product_options": {            
                "name": "New Checkout Test",
                "description": "a new checkout test",
                "media": ["https://google.com"],
                "redirect_url": "https://google.com",
                "receipt_button_text": "Text Receipt",
                "receipt_link_url": "https://lemonsqueezy.com",
                "receipt_thank_you_note": "Thanks to lemonsqueezy",
                "enabled_variants": [int(cast(str, self.variant_id))],
                "confirmation_title": "Thank you for your support",
                "confirmation_message": "Thank you for subscribing and have a great day",
                "confirmation_button_text": "View Order",
            },
            "checkout_options": {
                "embed": True,
                "media": True,
                "logo": True,
                "desc": True,
                "dark": True,
                "skip_trial": True,
                "discount": False,
                "button_color": "#ccc",
                "subscription_preview": True,
            },
            "checkout_data": {
                "email": "tita0x00@gmail.com",
                "name": "Lemon Squeezy Test",
                "billing_address": {                
                    "country": "US",
                },
                "tax_number": "12345",
                "custom": {
                    "user_id": "1234567890",
                    "user_name": "Mrs.A",
                    "nick_name": "AAA",
                },
                "variant_quantities": [],
            },
            "expires_at": None,
            "preview": True,
            "test_mode": True,
        }
        response = await create_checkout(
            cast(str, self.store_id),
            cast(str, self.variant_id),
            new_checkout
        )
        
        self.assertEqual(response.get('status_code'), 201)
        self.assertTrue(response.get('data'))
        self.assertIsNone(response.get('error'))

        data = response['data']['data']
        links = response['data']['links']
        self.assertTrue(data)
        self.assertTrue(links)

        _id = data['id']
        attributes = data['attributes']
        _type = data['type']
        relationships = data['relationships']

        self.assertTrue(_id)
        self.assertTrue(attributes)
        self.assertTrue(relationships)
        self.assertEqual(DATATYPE, _type)

        items = [
            attributes.get('store_id'),
            attributes.get('variant_id'),
            attributes.get('custom_price'),
            attributes.get('product_options'),
            attributes.get('checkout_options'),
            attributes.get('checkout_data'),
            attributes.get('preview'),
            attributes.get('expires_at'),
            attributes.get('created_at'),
            attributes.get('updated_at'),
            attributes.get('test_mode'),
            attributes.get('url'),
        ]

        for item in items:
            if item:
                self.assertTrue(item)
        
        self.assertEqual(len(items), len(attributes))
        self.assertEqual(
            int(cast(str, self.store_id)),
            attributes['store_id']
        )
        self.assertEqual(
            int(cast(str, self.variant_id)),
            attributes['variant_id']
        )

        product_items = [
            attributes['product_options'].get('name'),
            attributes['product_options'].get('description'),
            attributes['product_options'].get('media'),
            attributes['product_options'].get('redirect_url'),
            attributes['product_options'].get('receipt_button_text'),
            attributes['product_options'].get('receipt_link_url'),
            attributes['product_options'].get('receipt_thank_you_note'),
            attributes['product_options'].get('enabled_variants'),
            attributes['product_options'].get('confirmation_title'),
            attributes['product_options'].get('confirmation_message'),
            attributes['product_options'].get('confirmation_button_text'),
        ]
        for item in product_items:
            if item:
                self.assertTrue(item)
            
        self.assertEqual(len(product_items), len(attributes['product_options']))
        self.assertEqual(
            attributes['product_options'].get('name'),
            new_checkout['product_options']['name']
        )
        self.assertEqual(
            attributes['product_options'].get('description'),
            new_checkout['product_options']['description']
        )
        self.assertEqual(
            attributes['product_options'].get('receipt_button_text'),
            new_checkout['product_options']['receipt_button_text']
        )
        self.assertEqual(
            attributes['product_options'].get('receipt_thank_you_note'),
            new_checkout['product_options']['receipt_thank_you_note']
        )
        self.assertEqual(
            attributes['product_options'].get('receipt_link_url'),
            new_checkout['product_options']['receipt_link_url']
        )

        checkout_items = [
            attributes['checkout_options'].get('embed'),
            attributes['checkout_options'].get('media'),
            attributes['checkout_options'].get('logo'),
            attributes['checkout_options'].get('desc'),
            attributes['checkout_options'].get('discount'),
            attributes['checkout_options'].get('skip_trial'),
            attributes['checkout_options'].get('quantity'),
            attributes['checkout_options'].get('dark'),
            attributes['checkout_options'].get('subscription_review'),
            attributes['checkout_options'].get('button_color'),
        ]
        
        for item in checkout_items:
            if item:
                self.assertTrue(item)
        
        self.assertEqual(len(checkout_items), len(attributes['checkout_options']))
        self.assertEqual(
            attributes['checkout_options'].get('logo'),
            new_checkout['checkout_options']['logo']
        )
        self.assertEqual(
            attributes['checkout_options'].get('desc'),
            new_checkout['checkout_options']['desc']
        )
        self.assertEqual(
            attributes['checkout_options'].get('subscription_preview'),
            new_checkout['checkout_options']['subscription_preview']
        )
        self.assertEqual(
            attributes['checkout_options'].get('dark'),
            new_checkout['checkout_options']['dark']
        )
        self.assertEqual(
            attributes['checkout_options'].get('button_color'),
            new_checkout['checkout_options']['button_color']
        )

        checkout_data = [
            attributes['checkout_data'].get('email'),
            attributes['checkout_data'].get('name'),
            attributes['checkout_data'].get('billing_address'),
            attributes['checkout_data'].get('tax_number'),
            attributes['checkout_data'].get('discount_code'),
            attributes['checkout_data'].get('custom'),
            attributes['checkout_data'].get('variant_quantities'),
        ]

        for item in checkout_data:
            if item:
                self.assertTrue(item)
        
        self.assertEqual(len(checkout_data), len(attributes['checkout_data']))
        self.assertEqual(
            attributes['checkout_data'].get('email'),
            new_checkout['checkout_data']['email']
        )
        self.assertEqual(
            attributes['checkout_data'].get('name'),
            new_checkout['checkout_data']['name']
        )

        if preview := attributes['preview']:
            preview_items = [
                preview['currency'],
                preview['currency_rate'],
                preview['discount_total'],
                preview['discount_total_formatted'],
                preview['discount_total_usd'],
                preview['setup_fee'],
                preview['setup_fee_formatted'],
                preview['setup_fee_usd'],
                preview['subtotal'],
                preview['subtotal_formatted'],
                preview['subtotal_usd'],
                preview['tax'],
                preview['tax_formatted'],
                preview['tax_usd'],
                preview['total'],
                preview['total_formatted'],
                preview['total_usd'],
            ]

            for item in preview_items:
                if item:
                    self.assertTrue(item)
            
            self.assertEqual(len(preview_items), len(preview))
        
        variant = relationships['variant']
        store = relationships['store']

        self.assertTrue(variant['links'])
        self.assertTrue(store['links'])


    async def test_404_error_response_upon_creation_of_new_checkout(self):
        """Tests that it fails to create a new checkout when the wrong variant id
        is provided.
        """
        response = await create_checkout(
            cast(str, self.store_id),
            "123",
        )
        self.assertEqual(response.get('status_code'), 404)
        self.assertIsNotNone(response.get('error'))
    

class TestGetCheckout(unittest.IsolatedAsyncioTestCase):
    """Test the functionality of the `get_checkout` function."""

    def setUp(self) -> None:
        BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
        load_dotenv(os.path.join(BASE_DIR, '.env'))

        lemon_squeezy_setup(Config(
            api_key= os.getenv("LEMONSQUEEZY_API_KEY"),
        ))
        self.store_id = os.getenv("LEMONSQUEEZY_STORE_ID")
        self.variant_id = os.getenv("LEMONSQUEEZY_VARIANT_ID")
        self.checkout_id = os.getenv("LEMONSQUEEZY_CHECKOUT_ID")

    
    async def test_not_found_retrieval_of_checkout(self):
        """Tests the api responds with a 404 error code."""
        response = await get_checkout("notrealcheckoutid")
        self.assertEqual(response.get('status_code'), 404)
        self.assertIsNotNone(response.get('error'))
        self.assertIn('errors', cast(dict, response.get('data')))

    async def test_successful_retrival_of_checkout(self):
        """Tests the api responds with the wanted checkout object."""

        response = await get_checkout(cast(str, self.checkout_id))
        self.assertTrue(response.get('data'))
        self.assertIsNone(response.get('error'))
        self.assertEqual(response.get('status_code'), 200)

        id = response['data']['data']['id']
        self.assertEqual(self.checkout_id, id)
    
    async def test_successful_retrival_with_related_resource(self):
        response = await get_checkout(
            cast(str, self.checkout_id),
            {
                'include': ['store'],
            }
        )
        self.assertTrue(response.get('data'))
        self.assertIsNone(response.get('error'))
        self.assertEqual(response.get('status_code'), 200)

        id = response['data']['data']['id']
        store_id = response['data']['data']['attributes']['store_id']

        self.assertEqual(self.checkout_id, id)
        self.assertEqual(int(cast(str, self.store_id)), store_id)


class TestListCheckout(unittest.IsolatedAsyncioTestCase):
    """Test the functionality of the `list_checkout` function"""

    def setUp(self) -> None:
        BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
        load_dotenv(os.path.join(BASE_DIR, '.env'))

        lemon_squeezy_setup(Config(
            api_key= os.getenv("LEMONSQUEEZY_API_KEY"),
        ))
        self.store_id = os.getenv("LEMONSQUEEZY_STORE_ID")
        self.variant_id = os.getenv("LEMONSQUEEZY_VARIANT_ID")
    
    async def test_list_all_checkouts(self):
        """Tests that a paginated list of checkouts is returned"""
        response = await list_checkouts()
        self.assertTrue(response.get('data'))
        self.assertIsNone(response.get('error'))
        self.assertEqual(response.get('status_code'), 200)

        data: list = response['data']['data']
        links: dict = response['data']['links']
        meta: dict =  response['data']['meta']

        self.assertTrue(meta)
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
    
    async def test_include_parameter(self):
        """Test the API response when the `include` parameter is used."""
        response = await list_checkouts({
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
        """Tests the api responds with a list of checkouts filtered by store id."""
        response = await list_checkouts({
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

    async def test_filter_by_variant_id(self):
        """Tests the api responds with a list of checkouts filtered by store id."""
        response = await list_checkouts({
            "filter": {
                "variant_id": self.variant_id
            }
        })
        self.assertEqual(response.get('status_code'), 200)
        self.assertIsNone(response.get('error'))
        self.assertTrue(response.get('data'))

        data: list = response['data']['data']
        filtered_data = [
            item for item in filter(
                lambda x: x['attributes']['variant_id'] == int(
                    cast(str, self.variant_id)
                ),
                data
            )
        ]
        self.assertEqual(len(data), len(filtered_data))
    
    async def test_page_parameter(self):
        """Test the API response when the `page` parameter is used."""
        response = await list_checkouts({
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