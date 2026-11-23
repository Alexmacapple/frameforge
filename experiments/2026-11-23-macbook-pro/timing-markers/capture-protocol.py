import subprocess,time,json,pathlib,datetime
D=pathlib.Path('/tmp/frameforge-ff08-20261123');D.mkdir(exist_ok=True)
events=[]
def run(*args):
 p=subprocess.run(['agent-browser','--session','frameforge-v4',*args],capture_output=True,text=True,timeout=40)
 if p.returncode:raise RuntimeError(f'{args}: {p.stderr}')
 return p.stdout.strip()
def log(name,**kw):
 events.append(dict(event=name,mono_ns=time.monotonic_ns(),utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),**kw))
def marker(color,stage):
 log('marker_request',color=color,stage=stage)
 run('eval',f"(()=>{{let x=document.getElementById('ff-marker');if(!x){{x=document.createElement('div');x.id='ff-marker';x.style='position:fixed;top:0;left:0;width:100%;height:120px;z-index:2147483647';document.body.append(x)}}x.style.background='{color}';x.dataset.stage='{stage}'}})()")
 log('marker_return',color=color,stage=stage)
try:
 run('open','https://todomvc.com/examples/react/dist/')
 run('eval',"localStorage.clear();location.reload()")
 log('record_start_request')
 print(run('record','start',str(D/'capture.webm')),flush=True)
 log('record_start_return')
 time.sleep(.7)
 marker('#ff0000','baseline')
 time.sleep(.6)
 marker('#00ff00','start')
 time.sleep(.5)
 for i,(label,action,color) in enumerate([('Première tâche','add','#0000ff'),('Deuxième tâche','add','#ffff00'),('Première tâche','complete','#ff00ff')]):
  marker(color,f'action-{i+1}')
  log('action_begin',index=i+1,action=action)
  if action=='add':
   run('fill','input.new-todo',label);run('press','Enter')
  else:run('click','ul.todo-list li:first-child input.toggle')
  log('action_return',index=i+1)
  state=run('eval',"JSON.stringify([...document.querySelectorAll('ul.todo-list li')].map(x=>({text:x.innerText,done:x.classList.contains('completed')})))")
  log('assertion',index=i+1,state=state)
  print(i+1,state,flush=True)
  time.sleep(2)
 marker('#00ffff','end')
 time.sleep(.7)
 log('record_stop_request')
 print(run('record','stop'),flush=True)
 log('record_stop_return')
finally:
 try:run('close')
 except Exception:pass
 (D/'events.json').write_text(json.dumps(events,ensure_ascii=False,indent=2))
 print('events',len(events),flush=True)
