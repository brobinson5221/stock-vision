import type { Stock } from "./api";

const usd = new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" });
const ratio = new Intl.NumberFormat("en-US", { maximumFractionDigits: 2 });

export default function StockTable({ stocks }: { stocks: readonly Stock[] }) {
  return (
    <div className="table-scroll" tabIndex={0} role="region" aria-labelledby="stock-table-caption">
      <table>
        <caption id="stock-table-caption">Synthetic sample stocks · Amounts in USD</caption>
        <thead>
          <tr>
            <th scope="col">Symbol</th>
            <th scope="col">Company</th>
            <th scope="col">Sector</th>
            <th scope="col" className="numeric">Price (USD)</th>
            <th scope="col" className="numeric">Market cap (USD)</th>
            <th scope="col" className="numeric">P/E ratio</th>
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
