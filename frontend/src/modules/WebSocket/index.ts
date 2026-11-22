import { createWsConnection } from "./helper";
export const helloTest = createWsConnection<{ event: string; payload: string }>({
  url: "ws://localhost:4000/ws",
  key: "hello",
});
