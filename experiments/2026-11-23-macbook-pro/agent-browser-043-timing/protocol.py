import subprocess,time,json,pathlib
D=pathlib.Path('/tmp/frameforge-ff15-20261123');D.mkdir(exist_ok=True)
base=['npx','--yes','--package','agent-browser@0.43.0','agent-browser','--session','frameforge-043-timing']
events=[]
def run(*args):
 p=subprocess.run(base+list(args),capture_output=True,text=True,timeout=60)
 if p.returncode:raise RuntimeError(f'{args}: {p.stderr}')
 return p.stdout.strip()
def log(name,**kw):events.append(dict(event=name,monotonic_ns=time.monotonic_ns(),**kw))
def marker(color,stage):
 log('marker_request',stage=stage,color=color)
 run('eval',f"(()=>{{let x=document.getElementById('ff-marker');if(!x){{x=document.createElement('div');x.id='ff-marker';x.style='position:fixed;top:0;left:0;width:100%;height:70px;z-index:2147483647';document.body.append(x)}}x.style.background='{color}';x.dataset.stage='{stage}'}})()")
 log('marker_return',stage=stage,color=color)
try:
 run('open','https://todomvc.com/examples/react/dist/')
 run('eval','localStorage.clear();location.reload()')
 log('record_start_request')
 print(run('record','start',str(D/'timed.webm'),'--fps','30','--contact-sheet'),flush=True)
 log('record_start_return')
 time.sleep(.5)
 for i,(label,kind,pre,post) in enumerate([('Première tâche','add','#ff0000','#00ff00'),('Deuxième tâche','add','#0000ff','#ffff00'),('Première tâche','complete','#ff00ff','#00ffff')]):
  marker(pre,f'before-{i+1}')
  time.sleep(.3)
  log('action_begin',index=i+1)
  if kind=='add':run('fill','input.new-todo',label);run('press','Enter')
  else:run('click','ul.todo-list li:first-child input.toggle')
  log('action_return',index=i+1)
  state=run('eval',"JSON.stringify([...document.querySelectorAll('ul.todo-list li')].map(x=>({text:x.innerText,done:x.classList.contains('completed')})))")
  log('assertion',index=i+1,state=state)
  print(i+1,state,flush=True)
  marker(post,f'after-{i+1}')
  time.sleep(.5)
 log('record_stop_request')
 print(run('record','stop'),flush=True)
 log('record_stop_return')
finally:
 try:run('close')
 except Exception:pass
 (D/'events.json').write_text(json.dumps(events,ensure_ascii=False,indent=2))
