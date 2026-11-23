import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

const root = document.getElementById("root");
if (!root) throw new Error("Missing root element");

createRoot(root).render(
  <StrictMode>
    <main>
      <h1>Stock Vision</h1>
      <p>A stock screener using synthetic sample data.</p>
      <p>The stock table will be connected in the next step.</p>
    </main>
  </StrictMode>,
);
