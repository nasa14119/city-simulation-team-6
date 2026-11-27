#version 300 es
precision highp float;

in vec3 v_normalVector; 
in vec3 v_surfToLight; 
in vec3 v_surfToView; 
out vec4 outColor;
uniform vec4 u_ambientColor; 
uniform vec4 u_diffuseColor; 
uniform vec4 u_specularColor; 
uniform float u_shininess; 
uniform vec4 u_ambientLight; 
uniform vec4 u_diffuseLight; 
uniform vec4 u_specularLight;  

void main() {
    vec3 Nnormal = normalize(v_normalVector); 
    vec3 Nstol = normalize(v_surfToLight); 
    vec3 Nstov = normalize(v_surfToView); 
    vec3 reflection = 2.0*dot(Nnormal, Nstol) * Nnormal - Nstol; 
    float specularFactor = pow(max(dot(reflection, Nstov), 0.0), u_shininess); 
    
    vec4 ambient = u_ambientColor * u_ambientLight; 
    vec4 diffuse = u_diffuseColor * u_diffuseLight * max(dot(Nstol, Nnormal), 0.0); 
    vec4 specular = specularFactor * u_specularColor * u_specularLight; 
    outColor = ambient + diffuse + specular;
    //outColor = vec4(v_surfToLight, 1.0); 
}
