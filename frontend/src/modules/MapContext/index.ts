import { create } from "zustand";
import type { Map as MapType } from "./Nodes.types";

export type MapUpdateFn = (prev: MapType) => MapType;

type Store = {
  map: MapType;
  updateMap: (update: MapUpdateFn) => void;
};

export const Map = create<Store>()((set) => ({
  map: [],
  updateMap: (fn) => set(({ map: prevMap }) => ({ map: fn(prevMap) })),
}));
