import subprocess,time,json,pathlib
D=pathlib.Path('/tmp/frameforge-ff12-20261123');D.mkdir(exist_ok=True)
events=[]
def run(*args):
 p=subprocess.run(['agent-browser','--session','frameforge-clean',*args],capture_output=True,text=True,timeout=40)
 if p.returncode:raise RuntimeError(f'{args}: {p.stderr}')
 return p.stdout.strip()
def log(k,**v):events.append(dict(event=k,mono_ns=time.monotonic_ns(),**v))
try:
 run('open','https://todomvc.com/examples/react/dist/')
 run('eval','localStorage.clear();location.reload()')
 log('record_start_request');print(run('record','start',str(D/'clean.webm')),flush=True);log('record_start_return')
 time.sleep(.8)
 for i,(label,kind) in enumerate([('Première tâche','add'),('Deuxième tâche','add'),('Première tâche','complete')]):
  log('action_begin',index=i+1)
  if kind=='add':run('fill','input.new-todo',label);run('press','Enter')
  else:run('click','ul.todo-list li:first-child input.toggle')
  log('action_return',index=i+1)
  state=run('eval',"JSON.stringify([...document.querySelectorAll('ul.todo-list li')].map(x=>({text:x.innerText,done:x.classList.contains('completed')})))")
  log('assertion',index=i+1,state=state)
  print(i+1,state,flush=True)
  time.sleep(2)
 log('record_stop_request');print(run('record','stop'),flush=True);log('record_stop_return')
finally:
 try:run('close')
 except Exception:pass
 (D/'events.json').write_text(json.dumps(events,ensure_ascii=False,indent=2))
