# ruff: noqa: INP001 -- Tests live outside the installed src package.
from importlib.metadata import distribution

import stock_vision


def test_package_is_installed():
    assert distribution("stock-vision").metadata["Name"] == "stock-vision"  # noqa: S101
    assert stock_vision.__name__ == "stock_vision"  # noqa: S101
