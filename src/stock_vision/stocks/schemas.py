from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Stock(BaseModel):
    """Synthetic stock metrics; price and market capitalization are in USD."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        allow_inf_nan=False,
        strict=True,
        str_strip_whitespace=True,
    )

    symbol: str = Field(min_length=1, pattern=r"^[A-Z][A-Z0-9.-]*$")
    name: str = Field(min_length=1)
    sector: str = Field(min_length=1)
    price: float = Field(gt=0, description="USD per share")
    market_cap: float | None = Field(ge=0, description="USD; null when unavailable")
    pe_ratio: float | None = Field(description="Price/earnings ratio; null when unavailable")


class PageQuery(BaseModel):
    limit: int = Field(default=50, gt=0, le=100)
    offset: int = Field(default=0, ge=0)


class StockDataset(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    provenance: Literal["synthetic-sample"] = "synthetic-sample"
    currency: Literal["USD"] = "USD"
    items: tuple[Stock, ...]


class StockPage(StockDataset):
    total: int = Field(ge=0)
    limit: int = Field(gt=0, le=100)
    offset: int = Field(ge=0)
