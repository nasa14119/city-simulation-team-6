export const env = {
  BASE_WS: import.meta.env.PUBLIC_BACKEND_WS ?? "ws://localhost:4000",
  BASE_BACKEND: import.meta.env.PUBLIC_BACKEND_URL ?? "http://localhost:4000",
};
