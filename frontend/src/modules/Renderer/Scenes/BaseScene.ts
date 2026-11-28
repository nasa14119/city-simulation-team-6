import * as twgl from 'twgl-base.js'
import type { ShaderSource } from '@modules/Libs/Types';
import { Object3DProgram, Light3D, Camera3D } from '@modules/Libs/Objects';
import { M4, type Vec3, type Mat4 } from '@modules/Libs/Transformations/3d-lib.js'
import { SmartWs } from '@modules/WebSocket/helper.js'
import { env } from '@modules/config';

export abstract class BaseScene<T> {
  protected readonly gl: WebGL2RenderingContext;
  private readonly program: twgl.ProgramInfo;
  protected abstract readonly light: Light3D;
  protected abstract readonly camera: Camera3D;
  private oldTime: number = 0;
  protected queue: T[] = [];
  protected ws: SmartWs<T>;

  constructor(gl: WebGL2RenderingContext, shaders: ShaderSource) {
    this.gl = gl;
    twgl.resizeCanvasToDisplaySize(gl.canvas as HTMLCanvasElement);
    gl.viewport(0, 0, gl.canvas.width, gl.canvas.height);
    const { vs, fs } = shaders;
    this.program = twgl.createProgramInfo(gl, [vs, fs]);
    this.ws = new SmartWs<T>({
      url: `${env.BASE_WS}/ws`,
      onChangeConnection: (connected) => { console.log(`Connection state: ${connected ? "Up" : "Down"}`) },
      onMessage: (message) => this.queue.push(message)
    })
  }

  protected abstract render(deltaTime: number): void;
  protected abstract apply(message: T): void;
  protected drawObject(object: Object3DProgram, uniforms: Record<string, unknown>): void {
    this.gl.useProgram(object.programInfo.program);
    twgl.setUniforms(object.programInfo, uniforms);
    this.gl.bindVertexArray(object.vao);
    twgl.drawBufferInfo(this.gl, object.bufferInfo);
    //twgl.drawBufferInfo(this.gl, object.bufferInfo, gl.LINES);
  }

  onFrameRender() {

    const { gl } = this;

    // Clear the canvas
    gl.clearColor(0, 0, 0, 1);
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

    // Tell webgl to cull faces
    gl.enable(gl.CULL_FACE);
    gl.enable(gl.DEPTH_TEST);
  }
  draw = (newTime: number) => {
    const deltaTime = newTime - this.oldTime;
    this.oldTime = newTime;
    for (let message of this.getData()) {
      this.apply(message);
    }
    this.render(deltaTime);
    requestAnimationFrame(this.draw);
  }

  prepareObject(object: Object3DProgram, viewProjectionMatrix: Mat4): void {
    // Get the WebGL context and program info

    // Prepare the vector for translation and scale
    const v3_tra: Vec3 = object.posArray;
    const v3_sca: Vec3 = object.scaArray;

    // Create the individual transform matrices
    const scaMat: Mat4 = M4.scale(v3_sca);
    const rotXMat: Mat4 = M4.rotationX(object.transforms.rr.x);
    const rotYMat: Mat4 = M4.rotationY(object.transforms.rr.y);
    const rotZMat: Mat4 = M4.rotationZ(object.transforms.rr.z);
    const traMat: Mat4 = M4.translation(v3_tra);

    // Create the composite matrix with all transformations
    let transforms: Mat4 = M4.identity();
    transforms = M4.multiply(scaMat, transforms);
    transforms = M4.multiply(rotXMat, transforms);
    transforms = M4.multiply(rotYMat, transforms);
    transforms = M4.multiply(rotZMat, transforms);
    transforms = M4.multiply(traMat, transforms);

    // Apply the projection to the final matrix for the
    // World-View-Projection
    const wvpMat: Mat4 = M4.multiply(viewProjectionMatrix, transforms);

    // The matrix to be used for normal transformations
    const normalMat = M4.transpose(M4.inverse(transforms));

    let uniforms = {
      u_world: transforms,
      u_worldViewProjection: wvpMat,
      u_worldInverseTransform: normalMat,
      u_ambientColor: object.color,
      u_diffuseColor: object.color,
      u_specularColor: object.color,
      u_shininess: object.shininess,
    }

    this.drawObject(object, uniforms);
  }

  getData(): T[] {
    const messages = this.queue;
    this.queue = [];
    return messages;
  }
}
