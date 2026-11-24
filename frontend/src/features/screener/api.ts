export interface Stock {
  symbol: string;
  name: string;
  sector: string;
  price: number;
  market_cap: number | null;
  pe_ratio: number | null;
}

export interface StockPage {
  items: Stock[];
  total: number;
  limit: number;
  offset: number;
  provenance: "synthetic-sample";
  currency: "USD";
}

export type RangeMetric = "price" | "market_cap" | "pe_ratio";
export type RangeBound = `${"min" | "max"}_${RangeMetric}`;

export interface StockSort {
  sortBy: keyof Stock;
  sortDir: "asc" | "desc";
}

export interface StockQuery extends StockSort {
  limit: number;
  offset: number;
  q: string;
  sector: string;
  ranges: Partial<Record<RangeBound, string>>;
}

export class StockRangeError extends Error {}

function isStock(value: unknown): value is Stock {
  if (!value || typeof value !== "object") return false;
  const stock = value as Partial<Stock>;
  return (
    typeof stock.symbol === "string" && stock.symbol.length > 0 &&
    typeof stock.name === "string" && stock.name.length > 0 &&
    typeof stock.sector === "string" && stock.sector.length > 0 &&
    typeof stock.price === "number" && Number.isFinite(stock.price) && stock.price > 0 &&
    (stock.market_cap === null || (typeof stock.market_cap === "number" &&
      Number.isFinite(stock.market_cap) && stock.market_cap >= 0)) &&
    (stock.pe_ratio === null || (typeof stock.pe_ratio === "number" &&
      Number.isFinite(stock.pe_ratio)))
  );
}

export async function fetchStocks(signal: AbortSignal, query: StockQuery): Promise<StockPage> {
  const params = new URLSearchParams({
    limit: String(query.limit), offset: String(query.offset),
    sort_by: query.sortBy, sort_dir: query.sortDir,
  });
  const search = query.q.trim();
  if (search) params.set("q", search);
  if (query.sector) params.set("sector", query.sector);
  for (const [bound, value] of Object.entries(query.ranges)) {
    const number = value.trim();
    if (number) params.set(bound, number);
  }
  const response = await fetch(`/api/stocks?${params}`, { signal });
  if (response.status === 422) throw new StockRangeError("Invalid financial range.");
  if (!response.ok) throw new Error(`Stock request failed (${response.status}).`);
  const page: Partial<StockPage> | null = await response.json();
  if (
    !page || !Array.isArray(page.items) || !page.items.every(isStock) ||
    typeof page.total !== "number" || !Number.isSafeInteger(page.total) || page.total < 0 ||
    typeof page.limit !== "number" || !Number.isSafeInteger(page.limit) ||
    page.limit < 1 || page.limit > 100 ||
    typeof page.offset !== "number" || !Number.isSafeInteger(page.offset) || page.offset < 0 ||
    page.items.length > page.limit || page.items.length > page.total ||
    page.provenance !== "synthetic-sample" || page.currency !== "USD" ||
    page.offset !== query.offset || page.limit !== query.limit
  ) throw new Error("Invalid stock response.");
  return page as StockPage;
}
