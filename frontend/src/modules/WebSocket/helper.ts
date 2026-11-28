import { sleep } from "@modules/utils";
import { createStore } from "zustand/vanilla";
import { createJSONStorage } from "zustand/middleware";
import { persist } from "zustand/middleware";

type Props = {
  key: string;
  url: string;
};
type Store<M> = {
  message: M | null;
  setMessage: (mss: Store<M>["message"]) => void;
  isConnected: boolean;
};
type SmartWsConstructor<T> = {
  url: string;
  onChangeConnection: (isConnected: boolean) => void;
  onMessage: (mss: T) => void;
};

export class SmartWs<T> {
  ws: WebSocket;
  private closeNow = false;
  private delay: number;
  readonly url: string;
  private onChangeConnection: SmartWsConstructor<T>["onChangeConnection"];
  private onMessage: SmartWsConstructor<T>["onMessage"];
  constructor({ url, onChangeConnection: onChangeConection, onMessage }: SmartWsConstructor<T>) {
    this.url = url;
    this.onChangeConnection = onChangeConection;
    this.onMessage = onMessage;
    this.delay = 1;
    this.ws = new WebSocket(url);
    this.setup();
  }
  setup() {
    this.ws.onopen = () => {
      this.onChangeConnection(true);
      this.delay = 1;
    };
    this.ws.onclose = () => {
      this.onChangeConnection(false);
      this.delay = this.delay * 2;
      if (this.closeNow) return;
      this.reconnect();
    };
    this.ws.onmessage = (e) => {
      try {
        const mss = JSON.parse(e.data);
        this.onMessage(mss);
      } catch {
        console.error(`Error parsing ${e.data}`);
      }
    };
    this.ws.onerror = (e) => {
      console.error("Error in ws connection of:", e);
      this.ws.close();
    };
  }
  async reconnect() {
    console.log(`reconecting after ${this.delay}s`);
    await sleep(this.delay * 1000);
    if (this.closeNow) return;
    this.ws = new WebSocket(this.url);
    this.setup();
  }

  close() {
    this.closeNow = true;
    this.ws.close();
    return this.closeNow
  }
}

export function createWsConnection<T>({ key, url }: Props) {
  const store = createStore<Store<T>>()(
    persist(
      (set, get) => ({
        isConnected: false,
        message: get()?.message ?? null,
        setMessage: (mss) => set({ message: mss }),
      }),
      {
        name: key,
        storage: createJSONStorage(() => window.localStorage),
      },
    ),
  );
  new SmartWs<T>({
    url,
    onChangeConnection: (isOpen) => store.setState({ isConnected: isOpen }),
    onMessage: store.getState().setMessage,
  });
  return store;
}
