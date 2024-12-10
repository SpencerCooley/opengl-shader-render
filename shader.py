# Shader sources
vertex_shader_source = """
#version 120
attribute vec3 position;
void main() {
    gl_Position = vec4(position, 1.0);
}
"""

fragment_shader_source = """
#version 120
uniform vec2 resolution;
uniform float time;

// the uniforms can be passed to this shader program from the cpu from the code in main.py
// could be sensor data, mediapipe, camera, sound, etc.... 

float random(float x) {
    return fract(sin(x * 78.233) * 43758.5453);
}

vec2 center = vec2(0.5,0.5);
float speed = 0.035;

void main() {
    float invAr = resolution.y / resolution.x;
    vec2 uv = gl_FragCoord.xy / resolution; // Normalize coordinates (0.0 to 1.0)

    vec3 texcol;
    
    vec3 col = vec4(uv,0.5+0.1*sin(time),1.0).xyz;
	
    float x = (center.x-uv.x);
	float y = (center.y-uv.y) *invAr;
	//float r = -sqrt(x*x + y*y); //uncoment this line to symmetric ripples


    // this is what determines the field shape
	float r = -(x*x / y*y + x*uv.y);

    // simple circle field
    // float r = -(x*x + y*y);
    
	float z = 1.0 + 0.5*sin((r+time*speed)/0.013);
	
    texcol.x = z;
	texcol.y = z;
	texcol.z = z;

    gl_FragColor = vec4(col*texcol,1.0);
}

"""

