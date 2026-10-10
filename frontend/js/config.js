/* =========================================================
   config.js
   Single place to point the frontend at your backend server.
   Override at runtime by setting window.__BACKEND_URL__ before
   this script loads, or by adding <meta name="backend-url" ...>
   in index.html — useful when you deploy frontend/backend to
   different hosts.

   When served from the same origin (Render single-service),
   an empty string makes all fetches relative — works everywhere.
========================================================= */

const BACKEND_URL =
  window.__BACKEND_URL__ ||
  (document.querySelector('meta[name="backend-url"]') &&
    document.querySelector('meta[name="backend-url"]').content) ||
  "";

