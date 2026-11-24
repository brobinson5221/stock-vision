import type { Stock, StockSort } from "./api";

const usd = new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" });
const ratio = new Intl.NumberFormat("en-US", { maximumFractionDigits: 2 });

const columns = [
  { key: "symbol", label: "Symbol", numeric: false },
  { key: "name", label: "Company", numeric: false },
  { key: "sector", label: "Sector", numeric: false },
  { key: "price", label: "Price (USD)", numeric: true },
  { key: "market_cap", label: "Market cap (USD)", numeric: true },
  { key: "pe_ratio", label: "P/E ratio", numeric: true },
] as const;

export default function StockTable({ stocks, sort, busy, onSort }: {
  stocks: readonly Stock[];
  sort: StockSort;
  busy: boolean;
  onSort: (key: StockSort["sortBy"]) => void;
}) {
  return (
    <div className="table-scroll" tabIndex={0} role="region" aria-labelledby="stock-table-caption">
      <table aria-busy={busy}>
        <caption id="stock-table-caption">Synthetic sample stocks · Amounts in USD</caption>
        <thead>
          <tr>
            {columns.map(({ key, label, numeric }) => (
              <th key={key} scope="col" className={numeric ? "numeric" : undefined}
                aria-sort={sort.sortBy === key ? (sort.sortDir === "asc" ? "ascending" : "descending") : undefined}>
                <button className="table-sort" type="button" onClick={() => onSort(key)}>
                  {label}<span className="sort-indicator" aria-hidden="true" />
                </button>
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {stocks.map((stock) => (
            <tr key={stock.symbol}>
              <th scope="row">{stock.symbol}</th>
              <td>{stock.name}</td>
              <td>{stock.sector}</td>
              <td className="numeric">{usd.format(stock.price)}</td>
              <td className="numeric">{stock.market_cap === null ? "Unavailable" : usd.format(stock.market_cap)}</td>
              <td className="numeric">{stock.pe_ratio === null ? "Unavailable" : ratio.format(stock.pe_ratio)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
