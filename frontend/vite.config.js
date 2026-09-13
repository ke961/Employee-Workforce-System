import { defineConfig } from "vite";
import fs from "node:fs";
import path from "node:path";

function copyVanillaAssets() {
    return {
        name: "copy-vanilla-assets",
        closeBundle() {
            const distDir = path.resolve(__dirname, "dist");
            if (fs.existsSync(distDir)) {
                const jsDir = path.resolve(__dirname, "js");
                const cssDir = path.resolve(__dirname, "css");
                if (fs.existsSync(jsDir)) {
                    fs.cpSync(jsDir, path.join(distDir, "js"), { recursive: true });
                }
                if (fs.existsSync(cssDir)) {
                    fs.cpSync(cssDir, path.join(distDir, "css"), { recursive: true });
                }
            }
        },
    };
}

export default defineConfig({
    plugins: [copyVanillaAssets()],
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