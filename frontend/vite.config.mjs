import { defineConfig } from "vite";
import fs from "node:fs";
import { fileURLToPath } from "node:url";

const rootDir = fileURLToPath(new URL(".", import.meta.url));

function copyVanillaAssets() {
    return {
        name: "copy-vanilla-assets",
        closeBundle() {
            const distDir = path.resolve(rootDir, "dist");
            if (fs.existsSync(distDir)) {
                const jsDir = path.resolve(rootDir, "js");
                const cssDir = path.resolve(rootDir, "css");
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