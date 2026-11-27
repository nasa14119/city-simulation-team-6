import { V3 } from '@modules/Libs/Transformations/3d-lib.js';
import type { Color, VecXYZ } from '@modules/Libs/Types';

export class Light3D {
  id: number;
  position: VecXYZ;
  ambient: Color;
  diffuse: Color;
  specular: Color;

  constructor(
    id: number,
    position: number[] = [0, 0, 10],
    ambient: Color,
    diffuse: Color,
    specular: Color
  ) {
    this.id = id;
    // Initial transformations
    this.position = {
      x: position[0],
      y: position[1],
      z: position[2],
    };
    this.ambient = ambient;
    this.diffuse = diffuse;
    this.specular = specular;
  }

  // Return the position as an array
  get posArray() {
    return V3.create(this.position.x, this.position.y, this.position.z);
  }

  setColor(color: Color): void {
    this.diffuse = color;
    this.specular = color;
  }
}
