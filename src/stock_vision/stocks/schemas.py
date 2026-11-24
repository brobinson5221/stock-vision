from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, Field, FiniteFloat, model_validator


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
    q: str = Field(default="", max_length=100, description="Substring of symbol or company name")
    sector: str = Field(default="", max_length=100, description="Exact sector name")
    min_price: FiniteFloat | None = Field(default=None, ge=0)
    max_price: FiniteFloat | None = Field(default=None, ge=0)
    min_market_cap: FiniteFloat | None = Field(default=None, ge=0)
    max_market_cap: FiniteFloat | None = Field(default=None, ge=0)
    min_pe_ratio: FiniteFloat | None = None
    max_pe_ratio: FiniteFloat | None = None
    sort_by: Literal["symbol", "name", "sector", "price", "market_cap", "pe_ratio"] = "symbol"
    sort_dir: Literal["asc", "desc"] = "asc"

    @model_validator(mode="after")
    def validate_ranges(self) -> Self:
        for metric, lower, upper in (
            ("price", self.min_price, self.max_price),
            ("market_cap", self.min_market_cap, self.max_market_cap),
            ("pe_ratio", self.min_pe_ratio, self.max_pe_ratio),
        ):
            if lower is not None and upper is not None and lower > upper:
                message = f"min_{metric} must be less than or equal to max_{metric}"
                raise ValueError(message)
        return self


class StockDataset(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    provenance: Literal["synthetic-sample"] = "synthetic-sample"
    currency: Literal["USD"] = "USD"
    items: tuple[Stock, ...]


class StockPage(StockDataset):
    total: int = Field(ge=0)
    limit: int = Field(gt=0, le=100)
    offset: int = Field(ge=0)
