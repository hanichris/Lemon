from typing import Callable, NoReturn

from pydantic import BaseModel

from ..utils import CONFIG_KEY, set_kv, Error

class Config(BaseModel):
    api_key: str | None = None
    on_error: Callable[[Error], NoReturn] | None = None

def lemon_squeezy_setup(config: Config) -> Config:
    """Lemon Squeezy configuration.

    Args:
        config: the configuration object. Includes the api key and a callable
        if available to call if an error occurs.

    Returns:
        the configuraton object.
    """
    set_kv(
        CONFIG_KEY,
        {
            "api_key": config.api_key,
            "on_error": config.on_error
        }
    )
    return config
