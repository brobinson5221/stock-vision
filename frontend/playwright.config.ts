import { defineConfig } from "@playwright/test";

const previewUrl = "http://127.0.0.1:4173";

export default defineConfig({
  testDir: "./tests",
  outputDir: "../dist/e2e-results",
  use: { baseURL: previewUrl, trace: "retain-on-failure" },
  webServer: [
    {
      command: "uv run --locked python tests/e2e_server.py",
      cwd: "..",
      url: "http://127.0.0.1:8000/api/health",
    },
    {
      command: "npm run preview -- --host 127.0.0.1 --port 4173 --strictPort",
      url: previewUrl,
    },
  ],
});
