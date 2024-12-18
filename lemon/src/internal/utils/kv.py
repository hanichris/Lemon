from typing import Any


kv: dict[str, Any] = {}

def get_kv(key: str) -> Any | None:
    """Get the `value` corresponding to the `key` from the `kv` store.

    Args:
        key: String type key.

    Returns:
        `Value` corresponding to the `key` passed in. `None`, otherwise.
    """
    return kv.get(key)

def set_kv(key: str, value: Any) -> None:
    """Set the `value` corresponding to the `key` in the `kv` store.

    Args:
        key: String type key.
        value: The value to be set.
    """
    kv[key] = value

def clear_kv() -> None:
    """Deletes the contents of the `kv` store."""
    kv.clear()
