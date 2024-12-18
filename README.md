# LEMON SQUEEZY PYTHON SDK

## Introduction

This is an unofficial Python SDK for interacting with Lemon Squeezy, making it easy to incorporate billing into your Python application.

- Read [API Reference](https://docs.lemonsqueezy.com/api) to understand how the Lemon Squeezy API works.

This SDK closely follows the official JS SDK to enhance familiarity. You can visit the JS SDK
[Wiki page](https://github.com/lmsqueezy/lemonsqueezy.js/wiki) to better understand function usage.

## Features

This SDK relies on [Pydantic](https://docs.pydantic.dev/latest/) for type validation both in terms of the API's response and the requests made through the SDK.
Addtionally, it relies on the [httpx](https://www.python-httpx.org/) package to allow for simulataneous requests to be made with aid of the asyncio library.

For project management, [uv](https://docs.astral.sh/uv/) was employed.

> [!INFO]
>
> Not all of the features presented in the official JS SDK have been implemented.

## Installation

### Clone the repo

```bash
git clone https://github.com/hanichris/Lemon/tree/main
```

### Install the necessary dependencies

```bash
uv pip install -r pyproject.toml
```

### Create an API key

Create a new API key from [Settings > API](https://app.lemonsqueezy.com/settings/api) in your Lemon Squeezy Dashboard.

Add this API key into your project, for example as `LEMONSQUEEZY_API_KEY` in your `.env` file.

## Usage

```python
import asyncio
import os

from pprint import pprint
from pathlib import Path
from typing import cast

from dotenv import load_dotenv

from lemon.src.internal.setup import Config, lemon_squeezy_setup
from lemon.src.internal.utils import Error
from lemon.src.products import list_products

def err_fn(error: Error):
    raise RuntimeError(f"Lemon Squeezy API Error: {error.message}")

async def main():
    BASE_DIR = Path(__file__).resolve().parent

    load_dotenv(os.path.join(BASE_DIR, '.env'))

    lemon_squeezy_setup(Config(
        api_key= os.getenv("LEMONSQUEEZY_API_KEY"),
        on_error= err_fn,
    ))

    store_id = cast(str, os.getenv("LEMONSQUEEZY_STORE_ID"))

    products = await list_products({
        'filter': {
            'store_id': store_id,
        },
        'include': ['variants']
    })

    pprint(products)

if __name__ == "__main__":
    asyncio.run(main())

```
