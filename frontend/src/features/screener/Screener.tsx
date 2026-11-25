import { useEffect, useState } from "react";
import { fetchStocks, StockRangeError, type StockPage, type StockQuery } from "./api";
import RangeFilters from "./RangeFilters";
import StockTable from "./StockTable";

type State =
  | { status: "loading"; page?: StockPage }
  | { status: "error" }
  | { status: "invalid-range" }
  | { status: "ready"; page: StockPage };

// shortcut: sectors match the packaged sample, use API-provided options when the data source changes.
const sectors = ["Energy", "Healthcare", "Industrials", "Technology"];

export default function Screener() {
  const [attempt, setAttempt] = useState(0);
  const [query, setQuery] = useState<StockQuery>({
    limit: 50, offset: 0, q: "", sector: "", ranges: {}, sortBy: "symbol", sortDir: "asc",
  });
  const [state, setState] = useState<State>({ status: "loading" });
  const { offset, limit, q, sector } = query;
  const displayedPage = state.status === "ready" || state.status === "loading" ? state.page : undefined;
  const resultRange = displayedPage?.items.length
    ? `${displayedPage.offset + 1}–${displayedPage.offset + displayedPage.items.length}`
    : "0–0";

  function changeQuery(next: StockQuery, page?: StockPage) {
    setState({ status: "loading", page });
    setQuery(next);
  }

  function changeTextFilter(filter: "q" | "sector", value: string) {
    changeQuery({ ...query, offset: 0, [filter]: value });
  }

  useEffect(() => {
    const controller = new AbortController();
    fetchStocks(controller.signal, query).then(
      (page) => {
        if (!controller.signal.aborted) setState({ status: "ready", page });
      },
      (error: unknown) => {
        if (!controller.signal.aborted) {
          setState({ status: error instanceof StockRangeError ? "invalid-range" : "error" });
        }
      },
    );
    return () => controller.abort();
  }, [attempt, query]);

  return (
    <section aria-labelledby="stocks-heading">
      <h2 id="stocks-heading">Stocks</h2>
      <div className="stock-filters">
        <div>
          <label htmlFor="stock-search">Symbol or company</label>
          <input id="stock-search" type="search" maxLength={100} value={q}
            onChange={(event) => changeTextFilter("q", event.target.value)} />
        </div>
        <div>
          <label htmlFor="stock-sector">Sector</label>
          <select id="stock-sector" value={sector}
            onChange={(event) => changeTextFilter("sector", event.target.value)}>
            <option value="">All sectors</option>
            {sectors.map((option) => <option key={option}>{option}</option>)}
          </select>
        </div>
        <button type="button" onClick={() => changeQuery({ ...query, offset: 0, q: "", sector: "", ranges: {} })}>
          Clear filters
        </button>
      </div>
      <RangeFilters ranges={query.ranges} invalid={state.status === "invalid-range"}
        onChange={(bound, value) => changeQuery({
          ...query, offset: 0, ranges: { ...query.ranges, [bound]: value },
        })} />
      <button type="button" onClick={() => {
        setState({ status: "loading" });
        setAttempt((value) => value + 1);
      }}>
        Reload stocks
      </button>
      {state.status === "loading" && <p role="status">Loading stocks…</p>}
      {state.status === "error" && (
        <p role="alert">Unable to load stocks. Please try reloading.</p>
      )}
      {state.status === "ready" && <>
          <p role="status">
            Showing {resultRange} of {state.page.total} {state.page.total === 1 ? "stock" : "stocks"}.
          </p>
          {state.page.items.length === 0 && (
            <p>{state.page.total === 0 ? "No stocks found." : "No stocks on this page. Use Previous to return."}</p>
          )}
        </>}
      {displayedPage && displayedPage.items.length > 0 && (
        <StockTable stocks={displayedPage.items} sort={query} busy={state.status === "loading"}
          onSort={(sortBy) => changeQuery({
            ...query,
            offset: 0,
            sortBy,
            sortDir: query.sortBy === sortBy && query.sortDir === "asc" ? "desc" : "asc",
          }, displayedPage)} />
      )}
      <nav aria-label="Stock result pages" className="pagination">
        <button type="button" disabled={state.status === "loading" || offset === 0}
          onClick={() => changeQuery({ ...query, offset: Math.max(0, offset - limit) })}>
          Previous
        </button>
        <button type="button" disabled={state.status !== "ready" ||
          state.page.items.length === 0 || offset + limit >= state.page.total}
          onClick={() => changeQuery({ ...query, offset: offset + limit })}>
          Next
        </button>
      </nav>
    </section>
  );
}
