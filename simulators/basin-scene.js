/* Original illustrative basin. Rib dimensions and arc construction follow models/gen_rim.py, r4.
   Three.js 0.160.1 is distributed locally with its upstream licence in vendor/. */
function createBasin(canvas, values) {
  const T = THREE;
  const renderer = new T.WebGLRenderer({canvas, antialias:true, alpha:false});
  renderer.setPixelRatio(Math.min(devicePixelRatio, 1.6));
  const scene = new T.Scene(), artwork = new T.Group();
  scene.add(artwork);
  const camera = new T.PerspectiveCamera(32, 1, .05, 450);
  const vec = (x,y,z) => new T.Vector3(x,y,z);
  const U = value => ({value});
  const env = {sun:U(.25), dusk:U(1), seconds:U(0)};
  const noise = `
    float hash(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}
    float noise(vec2 p){vec2 i=floor(p), f=fract(p);f=f*f*(3.-2.*f);
      return mix(mix(hash(i),hash(i+vec2(1,0)),f.x),mix(hash(i+vec2(0,1)),hash(i+1.),f.x),f.y);}
    float fb(vec2 p){return .56*noise(p)+.28*noise(p*2.07+7.)+.16*noise(p*4.31+19.);}
  `;
  const worldVertex = `varying vec3 pos;
    void main(){pos=(modelMatrix*vec4(position,1.)).xyz;gl_Position=projectionMatrix*viewMatrix*vec4(pos,1.);}`;
  const sky = new T.Mesh(new T.SphereGeometry(280,48,24),new T.ShaderMaterial({
    side:T.BackSide,depthWrite:false,uniforms:env,vertexShader:worldVertex,
    fragmentShader:`varying vec3 pos;uniform float sun,dusk;${noise}
    void main(){
      vec3 d=normalize(pos-cameraPosition);float h=abs(d.y);
      vec3 zen=mix(vec3(.055,.088,.16),vec3(.31,.57,.73),sun);
      zen=mix(zen,vec3(.34,.38,.53),dusk);
      vec3 rim=mix(vec3(.19,.23,.32),vec3(.88,.89,.83),sun);
      rim=mix(rim,vec3(.98,.69,.52),dusk);
      vec3 col=mix(rim,zen,1.-exp(-h*4.1));
      vec2 c=d.xz/max(.055,h+.055);
      float cloud=fb(c*vec2(1.,2.6));
      col+= (.5-cloud)*.14*exp(-h*1.8);
      if(d.y>0.){
        vec2 skyUV=vec2(atan(d.x,-d.z),asin(d.y));
        vec2 cell=skyUV*410.;float star=hash(floor(cell));
        col+=vec3(.36,.40,.48)*smoothstep(.994,1.,star)*(1.-smoothstep(.06,.43,length(fract(cell)-.5)))*(1.-sun)*(1.-dusk)*smoothstep(.014,.13,h);
        float moon=length(skyUV-vec2(-.36,.105));
        col+=vec3(.83,.82,.74)*(1.-sun)*(1.-dusk)*(.68*(1.-smoothstep(.0036,.0047,moon))+.055*exp(-moon*69.));
      }
      float a=atan(d.x,d.z);float ridge=.001+.004*fb(vec2(a*27.,2.))+.0014*noise(vec2(a*230.,2.));
      col=mix(col,mix(vec3(.10,.16,.22),rim,.57),1.-smoothstep(ridge,ridge+.0012,h));
      gl_FragColor=vec4(col,1.);}`
  }));
  sky.renderOrder=-2;scene.add(sky);
  function mesh(geo, mat, x=0,y=0,z=0) {
    const m=new T.Mesh(geo,mat);m.position.set(x,y,z);artwork.add(m);return m;
  }
  const metal = (base, gloss) => new T.ShaderMaterial({
    uniforms:{...env,base:U(new T.Vector3(...base)),gloss:U(gloss),bandTone:U(vec(0,0,0)),bandLevel:U(0),bandCentre:U(0)},
    vertexShader:`varying vec3 n,p;varying float along;void main(){along=uv.x;p=(modelMatrix*vec4(position,1.)).xyz;
      n=normalize(mat3(modelMatrix)*normal);gl_Position=projectionMatrix*viewMatrix*vec4(p,1.);}`,
    fragmentShader:`varying vec3 n,p;varying float along;uniform vec3 base,bandTone;uniform float sun,dusk,gloss,bandLevel,bandCentre;
      void main(){vec3 N=normalize(n),V=normalize(cameraPosition-p);
      vec3 r=reflect(-V,N);float envY=r.y;
      // The second pass mirrors the model about the lake.
      if(p.y<-.08){envY=-envY;N.y=-N.y;}
      float lit=.25+.65*smoothstep(-.35,.45,envY)+.12*max(N.y,0.);
      float stripe=exp(-abs(envY-.07)*8.);
      vec3 sheen=mix(vec3(.62,.72,.85),vec3(1.,.80,.63),dusk);
      vec3 col=base*lit*(.53+.45*sun+.26*dusk)+gloss*sheen*(stripe*.35+.14*pow(1.-abs(dot(normalize(n),V)),2.));
      float spill=bandLevel*(1.-smoothstep(.025,.11,abs(along-bandCentre)));
      gl_FragColor=vec4(mix(col,bandTone,spill*.62),1.);}`
  });
  const grey=metal([.33,.39,.40],.38),socket=metal([.56,.45,.32],.55);
  const profile=[];
  for(const [r,y,start] of [[3.59,.013,0],[3.11,.013,90],[3.11,-.007,180],[3.59,-.007,270]]){
    for(let i=0;i<=6;i++){const a=(start+i*15)*Math.PI/180;profile.push(new T.Vector2(r+.06*Math.cos(a),y+.06*Math.sin(a)));}
  }
  profile.push(profile[0]);mesh(new T.LatheGeometry(profile,160),grey);
  const strips=[];
  values.forEach(({set,k,lean,rise,color})=>{
    const yaw=set*25*Math.PI/180, tilt=lean*Math.PI/180, d=k*.9;
    const half=Math.sqrt(3.35**2-d*d), radius=(half*half+rise*rise)/(2*rise), end=Math.asin(half/radius);
    function path(off,from,to){
      const curve=new T.Curve();
      curve.getPoint=t=>{
        const a=from+(to-from)*t, u=(radius+off)*Math.sin(a), v=(radius+off)*Math.cos(a)-radius+rise;
        const lateral=d+v*Math.sin(tilt);
        return vec(u*Math.cos(yaw)-lateral*Math.sin(yaw),.073+v*Math.cos(tilt),-u*Math.sin(yaw)-lateral*Math.cos(yaw));
      };
      return curve;
    }
    const tube=(curve,r,mat,n)=>mesh(new T.TubeGeometry(curve,n,r,16,false),mat);
    const brass=metal([.86,.66,.41],.9);
    Object.assign(brass.uniforms,{bandTone:U(vec(...color)),bandLevel:U(0),bandCentre:U(0)});
    tube(path(0,-end,end),.0762,brass,100);
    for(const sign of [-1,1])tube(path(0,sign*end,sign*(end-.3/radius)),.086,socket,8);
    const mat=new T.ShaderMaterial({uniforms:{...env,tone:U(vec(...color)),power:U(0),progress:U(0)},
      vertexShader:`varying float t;void main(){t=uv.x;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}`,
      fragmentShader:`varying float t;uniform vec3 tone;uniform float power,progress,sun,dusk;
        void main(){float b=1.-smoothstep(.035,.098,abs(t-progress));
        gl_FragColor=vec4(mix(vec3(.21,.19,.17)*(.65+sun*.7+dusk*.35),tone,power*b),1.);}`});
    const trim=end-.31/radius;
    for(const off of [-.0712,.0712])tube(path(off,-trim,trim),.015,mat,96);
    strips.push({strip:mat.uniforms,rib:brass.uniforms,trimRatio:trim/end});
  });
  for(const deg of [59,69,79,101,111,121]){
    const a=deg*Math.PI/180;
    mesh(new T.BoxGeometry(.5,.02,.3),grey,3.35*Math.cos(a),.085,-3.35*Math.sin(a)).rotation.y=a-Math.PI/2;
  }
  mesh(new T.CylinderGeometry(.024,.024,.9,12),grey,0,.523,-3.55);
  mesh(new T.CylinderGeometry(.065,.065,.13,16),metal([.82,.84,.78],.6),0,1.038,-3.55);
  const target=new T.WebGLRenderTarget(800,500,{minFilter:T.LinearFilter,magFilter:T.LinearFilter});
  const lakeUniforms={...env, mirror:U(target.texture), size:U(new T.Vector2()),waves:U(.15)};
  const water=new T.Mesh(new T.PlaneGeometry(420,420),new T.ShaderMaterial({
    uniforms:lakeUniforms,vertexShader:worldVertex,fragmentShader:`
    varying vec3 pos;uniform sampler2D mirror;uniform vec2 size;uniform float waves,sun,dusk,seconds;${noise}
    void main(){
      vec2 uv=gl_FragCoord.xy/size;float t=seconds*.31;
      float dist=length(cameraPosition-pos);float lod=1./(1.+.025*dist);
      vec2 p=pos.xz;float sw=fb(p*.72+vec2(t*.09,0.));
      float phase=p.y*14.+sw*10.+t*1.8+1.7*sin(p.x*1.7+t*.3);
      float w=sin(phase)*.52+.28*sin(p.y*24.-p.x*2.1+t*2.4+sw*6.)+.2*sin(p.x*5.+p.y*5.-t);
      w*=lod*smoothstep(.0,.55,lod);
      vec2 offset=vec2((sw-.5)*.019,w*.014)*(waves+.11);
      vec3 refl=texture2D(mirror,clamp(uv+offset,.001,.999)).rgb;
      vec3 deep=mix(vec3(.045,.095,.14),vec3(.18,.35,.39),sun);
      deep=mix(deep,vec3(.22,.32,.38),dusk);
      float grazing=1.-max(0.,normalize(cameraPosition-pos).y);
      float mixR=.09+.69*pow(grazing,1.65);
      vec3 col=mix(deep,refl,mixR);
      col+=vec3(.78,.84,.86)*(w*.045+(.5-sw)*.05)*(.6+sun*.3+dusk*.4);
      gl_FragColor=vec4(col,1.);}`
  }));
  water.rotation.x=-Math.PI/2;scene.add(water);
  let lastView, lastWidth, lastHeight,lastX,lastY;
  return function draw(state){
    const {minute,seconds,view,orbitX,orbitY,waves,levels,progress}=state;
    const w=canvas.clientWidth,h=canvas.clientHeight;
    if(!w||!h)return;
    if(w!==lastWidth||h!==lastHeight){
      renderer.setSize(w,h,false);renderer.getDrawingBufferSize(lakeUniforms.size.value);
      target.setSize(Math.ceil(lakeUniforms.size.value.x*.85),Math.ceil(lakeUniforms.size.value.y*.85));
      camera.aspect=w/h;camera.updateProjectionMatrix();lastWidth=w;lastHeight=h;lastView=undefined;
    }
    if(view!==lastView||orbitX!==lastX||orbitY!==lastY){
      const [x,y,z]=[[.65,2.05,11.8],[7,4.3,9],[0,13,.02]][view];
      const scale=Math.max(1,1.38/camera.aspect);
      const focus=view===2?0:.5;
      const s=new T.Spherical().setFromVector3(vec(x*scale,y*scale-focus,z*scale));
      s.theta+=orbitX;s.phi=T.MathUtils.clamp(s.phi-orbitY,.002,1.53);
      camera.position.setFromSpherical(s);camera.position.y+=focus;camera.lookAt(0,focus,0);
      lastX=orbitX;lastY=orbitY;lastView=view;
    }
    const solar=Math.cos((minute/60-12)*Math.PI/12);
    env.sun.value=T.MathUtils.smoothstep(solar,-.45,.45);
    env.dusk.value=Math.exp(-Math.pow((solar+.30)/.29,2));
    env.seconds.value=seconds;lakeUniforms.waves.value=waves;
    strips.forEach(({strip,rib,trimRatio},i)=>{
      strip.power.value=rib.bandLevel.value=levels[i];strip.progress.value=progress;
      rib.bandCentre.value=.5+(progress-.5)*trimRatio;
    });
    water.visible=false;artwork.scale.y=-1;renderer.setRenderTarget(target);renderer.render(scene,camera);
    artwork.scale.y=1;water.visible=true;renderer.setRenderTarget(null);renderer.render(scene,camera);
  };
}
