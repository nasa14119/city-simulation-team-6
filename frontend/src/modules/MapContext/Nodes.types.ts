type Cors2D = {
  x: number;
  y: number;
};

type Street = {
  type: "street";
  agents: {
    id: string;
  }[];
};

type Building = {
  type: "building";
  door_node: Cors2D;
  data: {
    position: Cors2D;
    height: number;
  };
};

type Empty = {
  type: "empty";
};

export type Node = Street | Building | Empty;

export type Map = Node[] | [];
