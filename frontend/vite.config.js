import { defineConfig } from "vite";

export default defineConfig({
    // ── Build settings ────────────────────────────────────
    build: {
        outDir: "dist",
        emptyOutDir: true,
        rollupOptions: {
            input: {
                main: "./index.html",
                login: "./login.html",
            },
        },
    },

    // ── Dev server (local only) ───────────────────────────
    server: {
        host: "127.0.0.1",
        port: 5173,

        proxy: {
            "/api": {
                target: "http://127.0.0.1:8000",
                changeOrigin: true
            }
        }
    }
});