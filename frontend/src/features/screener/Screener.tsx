import { useEffect, useState } from "react";
import { fetchStocks, type StockPage } from "./api";

type State =
  | { status: "loading" }
  | { status: "error" }
  | { status: "ready"; page: StockPage };

export default function Screener() {
  const [attempt, setAttempt] = useState(0);
  const [state, setState] = useState<State>({ status: "loading" });

  useEffect(() => {
    const controller = new AbortController();
    setState({ status: "loading" });
    fetchStocks(controller.signal).then(
      (page) => {
        if (!controller.signal.aborted) setState({ status: "ready", page });
      },
      () => {
        if (!controller.signal.aborted) setState({ status: "error" });
      },
    );
    return () => controller.abort();
  }, [attempt]);

  return (
    <section aria-labelledby="stocks-heading">
      <h2 id="stocks-heading">Stocks</h2>
      <button type="button" onClick={() => setAttempt((value) => value + 1)}>
        Reload stocks
      </button>
      {state.status === "loading" && <p role="status">Loading stocks…</p>}
      {state.status === "error" && (
        <p role="alert">Unable to load stocks. Please try reloading.</p>
      )}
      {state.status === "ready" && (
        state.page.items.length === 0 ? <p role="status">No stocks found.</p> : <>
          <p role="status">Showing {state.page.items.length} of {state.page.total} stocks.</p>
          <ul>
            {state.page.items.map((stock) => (
              <li key={stock.symbol}>{stock.symbol}: {stock.name}</li>
            ))}
          </ul>
        </>
      )}
    </section>
  );
}
