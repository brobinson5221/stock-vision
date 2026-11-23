import { useEffect, useState } from "react";
import { fetchStocks, type StockPage } from "./api";
import StockTable from "./StockTable";

type State =
  | { status: "loading" }
  | { status: "error" }
  | { status: "ready"; page: StockPage };

export default function Screener() {
  const [attempt, setAttempt] = useState(0);
  const [query, setQuery] = useState(() => new URLSearchParams({ limit: "50", offset: "0" }));
  const [state, setState] = useState<State>({ status: "loading" });
  const offset = Number(query.get("offset"));
  const limit = Number(query.get("limit"));

  function changePage(nextOffset: number) {
    const next = new URLSearchParams(query);
    next.set("offset", String(nextOffset));
    setState({ status: "loading" });
    setQuery(next);
  }

  useEffect(() => {
    const controller = new AbortController();
    fetchStocks(controller.signal, query).then(
      (page) => {
        if (!controller.signal.aborted) setState({ status: "ready", page });
      },
      () => {
        if (!controller.signal.aborted) setState({ status: "error" });
      },
    );
    return () => controller.abort();
  }, [attempt, query]);

  return (
    <section aria-labelledby="stocks-heading">
      <h2 id="stocks-heading">Stocks</h2>
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
            Showing {state.page.items.length ? state.page.offset + 1 : 0}–{state.page.items.length ? state.page.offset + state.page.items.length : 0} of {state.page.total} stocks.
          </p>
          {state.page.items.length === 0
            ? <p>{state.page.total === 0 ? "No stocks found." : "No stocks on this page. Use Previous to return."}</p>
            : <StockTable stocks={state.page.items} />}
        </>}
      <nav aria-label="Stock result pages" className="pagination">
        <button type="button" disabled={state.status === "loading" || offset === 0}
          onClick={() => changePage(Math.max(0, offset - limit))}>
          Previous
        </button>
        <button type="button" disabled={state.status !== "ready" ||
          state.page.items.length === 0 || offset + limit >= state.page.total}
          onClick={() => changePage(offset + limit)}>
          Next
        </button>
      </nav>
    </section>
  );
}
