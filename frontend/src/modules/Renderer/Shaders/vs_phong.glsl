#version 300 es
in vec4 a_position;
in vec4 a_normal; 

uniform mat4 u_worldViewProjection;

//Uniforms for ligthing 
uniform mat4 u_world; 
uniform mat4 u_worldInverseTransform; 
uniform vec3 u_lightWorldPosition; 
uniform vec3 u_viewWorldPosition;  
out vec3 v_normalVector; 
out vec3 v_surfToLight; 
out vec3 v_surfToView; 

void main() {
    //Normal vector to the surface
    v_normalVector = (u_worldInverseTransform * a_normal).xyz; 
    
    // Light position from a point
    vec3 transformedPos = (u_world * a_position).xyz; 
    v_surfToLight = u_lightWorldPosition - transformedPos; 
    v_surfToView = u_viewWorldPosition - transformedPos; 

    gl_Position = u_worldViewProjection * a_position;
}
