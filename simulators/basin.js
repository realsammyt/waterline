'use strict';
(() => {
  const values = [
    {name:'Warmth', set:-1,k:-1,lean:25,rise:1.15,color:[.96,.38,.70]},
    {name:'Leaf', set:1,k:1,lean:10,rise:1.55,color:[1,.84,.57]},
    {name:'Water', set:1,k:0,lean:10,rise:1.85,color:[1,.55,.40]},
    {name:'Time', set:1,k:-1,lean:10,rise:1.7,color:[1,.66,.34]},
    {name:'Air', set:-1,k:0,lean:25,rise:1.3,color:[1,.66,.75]},
    {name:'Sweetness', set:-1,k:1,lean:25,rise:1,color:[.77,.65,.96]}
  ];
  const order=[0,2,4,5,3,1], reduced=matchMedia('(prefers-reduced-motion: reduce)');
  const $=id=>document.getElementById(id);
  const zero=()=>Array(6).fill(0);
  let minute=1164, seconds=0, view=0, playing=false, last=performance.now(), dirty=true;
  let wakeStart=0, pending=zero();
  let previewEnd=null;
  const samples=new Set([19,22]);
  const hours=new Map([[19,[0,0,4,0,2,0]],[22,[0,0,0,3,0,4]]]);
  function select(group,index){
    Array.from($(group).children).forEach((b,i)=>b.setAttribute('aria-pressed',String(i===index)));
  }
  function group(id,fn){Array.from($(id).children).forEach((b,i)=>b.onclick=()=>fn(i));}
  function stop(){playing=false;$('play').textContent='▶  Play cycle';}
  function seek(m){previewEnd=null;minute=m;dirty=true;update();}
  function play(){playing=true;last=performance.now();$('play').textContent='Ⅱ  Pause cycle';}
  group('times',i=>{stop();seek([720,1164,1350][i]);});
  let orbitX=0,orbitY=0,drag=null;
  function orbit(dx,dy){
    orbitX+=dx;orbitY=Math.max(-1.5,Math.min(1.5,orbitY+dy));
    dirty=true;update();
  }
  const canvas=$('view');
  canvas.onpointerdown=e=>{
    if(!e.isPrimary||e.button!==0)return;
    drag=[e.clientX,e.clientY];canvas.setPointerCapture(e.pointerId);
  };
  canvas.onpointermove=e=>{
    if(!drag||!e.isPrimary)return;
    orbit((drag[0]-e.clientX)*.007,(e.clientY-drag[1])*.005);
    drag=[e.clientX,e.clientY];
  };
  canvas.onlostpointercapture=()=>{drag=null;};
  canvas.onkeydown=e=>{
    const delta={ArrowLeft:[-.08,0],ArrowRight:[.08,0],ArrowUp:[0,.06],ArrowDown:[0,-.06]}[e.key];
    if(delta){e.preventDefault();orbit(...delta);}
  };
  group('views',i=>{view=i;orbitX=0;orbitY=0;dirty=true;update();});
  $('time').oninput=e=>{stop();seek(Number(e.target.value));};
  $('play').onclick=()=>{
    if(playing)stop();
    else play();
  };
  $('surface').onchange=()=>{wakeStart=seconds;dirty=true;};
  function refreshChoices(){
    Array.from($('choices').children).forEach((button,i)=>{
      button.lastChild.textContent=pending[i]+' +';
      button.setAttribute('aria-label','Add a choice for '+values[i].name+', '+pending[i]+' queued');
    });
  }
  values.forEach(({name},i)=>{
    const button=document.createElement('button');button.className='vote';
    const label=document.createElement('span');label.textContent=name;
    button.append(document.createElement('i'),label,document.createElement('span'));
    button.onclick=()=>{pending[i]++;refreshChoices();};
    $('choices').append(button);
    $('visitor-value').add(new Option(name,String(i)));
  });
  refreshChoices();
  $('clear').onclick=()=>{pending=zero();refreshChoices();};
  function startHour(hour){
    hours.set(hour,pending);pending=zero();samples.delete(hour);refreshChoices();
  }
  const meanings=[
    'Welcome someone who arrived today.', 'Remember where you came from.',
    'Care for the lake and what we share.', 'Slow down or remember someone.',
    'Make room to breathe or speak.', 'Celebrate something from today.'
  ];
  $('visitor-value').onchange=()=>{
    const selected=$('visitor-value').value;
    $('visitor-show').disabled=selected==='';
    $('visitor-meaning').textContent=meanings[selected] || 'Try this at dusk or night to see the coloured band.';
  };
  $('visitor-show').onclick=()=>{
    const selected=$('visitor-value').value;
    if(selected==='')return;
    stop();
    const hour=(Math.floor(minute/60)+1)%24;
    pending[selected]++;
    startHour(hour);
    seek(hour*60);
    const receipt='You chose '+values[selected].name+' for '+String(hour).padStart(2,'0')+':00. ';
    if(lighting().phase==='Day'){
      $('visitor-receipt').textContent=receipt+'Decorative lights are off in daylight. Choose Dusk to try the night score.';
    }else if(reduced.matches){
      seek(hour*60+6);
      $('visitor-receipt').textContent=receipt+'Opening order: '+order.map(i=>values[i].name).join(', ')+'. The band is paused at its starting foot. Press Play cycle to watch it travel.';
      previewEnd=hour*60+59.99;
    }else{
      previewEnd=hour*60+59.99;
      $('visitor-receipt').textContent=receipt+'Watch the thread cross the six ribs, then follow the held band from foot to foot.';
      play();
    }
    $('visitor-value').value='';
    $('visitor-value').onchange();
    canvas.focus({preventScroll:true});
    $('stage').scrollIntoView({block:'center'});
  };
  $('next').onclick=()=>{
    const hour=(Math.floor(minute/60)+1)%24;startHour(hour);seek(hour*60);
    if(!reduced.matches&&!playing)$('play').click();
  };
  function lighting(){
    const hour=Math.floor(minute/60), elapsed=minute%60, counts=hours.get(hour)||zero();
    const high=Math.max(...counts),levels=zero();
    const phase=minute<300||minute>=1260?'Night':minute<420||minute>=1080?'Dusk':'Day';
    const names=[];
    let message,progress;
    if(phase==='Day'){message='Daylight. Decorative strips are off.';progress=0;}
    else if(elapsed<6){
      const step=Math.floor(elapsed), fraction=elapsed-step;
      levels[order[step]]=reduced.matches?1:Math.sin(Math.PI*fraction)**.65;
      progress=reduced.matches?.5:fraction;
      message='Opening thread · '+values[order[step]].name+' ('+(step+1)+' of 6)';
    }else{
      progress=.035+.93*(elapsed-6)/54;
      counts.forEach((n,i)=>{
        if(high&&2*n>=high){levels[i]=n===high?1:.66*n/high+.12;names.push(values[i].name+(n===high?'':' (dimmer)'));}
      });
      message=(samples.has(hour)?'Example chord · ':'')+(names.join(' + ')||'Quiet hour. No choices held.');
    }
    return {phase,message,levels,progress};
  }
  function update(){
    const {phase,message}=lighting();
    const clock=[Math.floor(minute/60),Math.floor(minute%60)].map(n=>String(n).padStart(2,'0')).join(':');
    $('clock').value=clock;$('time').value=Math.floor(minute);$('time').setAttribute('aria-valuetext',clock);
    const custom=Math.abs(orbitX)+Math.abs(orbitY)>.001;
    select('views',custom?-1:view);
    $('readout').textContent=phase+' · '+(custom?'Orbit':['Shore','Oblique','Above'][view]);
    $('viewnumber').textContent='VIEW 0'+(view+1);
    if($('score').textContent!==message)$('score').textContent=message;
    $('view-score').textContent=message;
    select('times',['Day','Dusk','Night'].indexOf(phase));
  }
  let draw=null, contextLost=false;
  function fallback(){$('fallback').hidden=false;}
  function setup(){
    try{draw=createBasin($('view'),values);$('fallback').hidden=true;dirty=true;}catch(e){fallback();}
  }
  $('view').addEventListener('webglcontextlost',e=>{e.preventDefault();contextLost=true;fallback();});
  $('view').addEventListener('webglcontextrestored',()=>{contextLost=false;dirty=true;$('fallback').hidden=Boolean(draw);});
  setup();update();
  new ResizeObserver(()=>{dirty=true;}).observe($('stage'));
  reduced.addEventListener('change',()=>{stop();dirty=true;});
  function frame(now){
    const dt=Math.min(.25,(now-last)/1000);last=now;
    if(!document.hidden){
      if(!reduced.matches)seconds+=dt;
      if(playing){
        const oldHour=Math.floor(minute/60),oldMinute=Math.floor(minute);
        let speed=Number($('speed').value);
        if(previewEnd!==null && minute%60<6)speed=Math.min(1,speed);
        let next=minute+dt*speed;
        if(previewEnd!==null && next>=previewEnd){
          next=previewEnd;previewEnd=null;stop();dirty=true;
        }
        minute=next%1440;
        if(Math.floor(minute/60)!==oldHour)startHour(Math.floor(minute/60));
        if(oldMinute!==Math.floor(minute))update();
      }
      if(draw&&!contextLost&&(dirty||playing||!reduced.matches)){
        const surface=$('surface').selectedIndex;
        const age=reduced.matches?2:seconds-wakeStart;
        const waves=surface===0?.12:surface===1?1.3:.12+3.2*Math.exp(-((age-2)**2)/9);
        draw({minute,seconds,view,orbitX,orbitY,waves,...lighting()});dirty=false;
      }
    }
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
})();
