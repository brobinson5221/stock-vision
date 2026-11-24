import type { RangeBound, RangeMetric, StockQuery } from "./api";

const metrics = [
  ["price", "Price (USD)"],
  ["market_cap", "Market cap (USD)"],
  ["pe_ratio", "P/E ratio"],
] as const satisfies ReadonlyArray<readonly [RangeMetric, string]>;

export default function RangeFilters({ ranges, invalid, onChange }: {
  ranges: StockQuery["ranges"];
  invalid: boolean;
  onChange: (bound: RangeBound, value: string) => void;
}) {
  return (
    <>
      <div className="stock-filters">
        {metrics.map(([metric, label]) => (
          <fieldset className="stock-range" key={metric}>
            <legend>{label}</legend>
            <div className="stock-range-bounds">
              {(["min", "max"] as const).map((edge) => {
                const bound: RangeBound = `${edge}_${metric}`;
                const id = `stock-${bound}`;
                return (
                  <div key={bound}>
                    <label htmlFor={id}>{edge === "min" ? "Minimum" : "Maximum"}</label>
                    <input id={id} type="text" inputMode={metric === "pe_ratio" ? "text" : "decimal"}
                      value={ranges[bound] ?? ""}
                      aria-describedby={invalid ? "stock-range-error" : undefined}
                      onChange={(event) => onChange(bound, event.target.value)} />
                  </div>
                );
              })}
            </div>
          </fieldset>
        ))}
      </div>
      {invalid && (
        <p id="stock-range-error" role="alert">
          Enter finite numbers or leave a bound blank. Price and market cap must be zero or higher.
          Each minimum must be at most its maximum.
        </p>
      )}
    </>
  );
}
