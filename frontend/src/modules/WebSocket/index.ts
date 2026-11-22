import { env } from "@modules/config";
import { createWsConnection } from "./helper";

export const helloTest = createWsConnection<{ event: string; payload: string }>({
  url: `${env.BASE_WS}/ws`,
  key: "hello",
});
