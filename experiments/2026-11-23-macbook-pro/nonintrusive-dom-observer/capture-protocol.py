import subprocess,time,json,pathlib
D=pathlib.Path('/tmp/frameforge-ff13-20261123');D.mkdir(exist_ok=True)
events=[]
def run(*args):
 p=subprocess.run(['agent-browser','--session','frameforge-v7',*args],capture_output=True,text=True,timeout=40)
 if p.returncode:raise RuntimeError(f'{args}: {p.stderr}')
 return p.stdout.strip()
def log(k,**v):events.append(dict(event=k,mono_ns=time.monotonic_ns(),**v))
try:
 run('open','https://todomvc.com/examples/react/dist/')
 run('eval','localStorage.clear();location.reload()')
 log('record_start_request');print(run('record','start',str(D/'clean-observed.webm')),flush=True);log('record_start_return')
 # The recording command may navigate/reload: install observer AFTER start.
 js="""(()=>{window.__ffEvents=[];window.__ffBase=performance.now();let last='';const scan=()=>{let rows=[...document.querySelectorAll('ul.todo-list li')].map(x=>({text:x.innerText,done:x.classList.contains('completed')}));let state=JSON.stringify(rows);if(state!==last){last=state;window.__ffEvents.push({kind:'dom_state',relative_ms:performance.now()-window.__ffBase,rows})}};window.__ffObserver=new MutationObserver(scan);window.__ffObserver.observe(document.body,{childList:true,subtree:true,attributes:true,characterData:true});scan();return window.__ffBase})()"""
 print('observer',run('eval',js),flush=True)
 time.sleep(.8)
 for i,(label,kind) in enumerate([('Première tâche','add'),('Deuxième tâche','add'),('Première tâche','complete')]):
  log('action_begin',index=i+1)
  if kind=='add':run('fill','input.new-todo',label);run('press','Enter')
  else:run('click','ul.todo-list li:first-child input.toggle')
  log('action_return',index=i+1)
  state=run('eval',"JSON.stringify([...document.querySelectorAll('ul.todo-list li')].map(x=>({text:x.innerText,done:x.classList.contains('completed')})))")
  log('assertion',index=i+1,state=state)
  print(i+1,state,flush=True)
  time.sleep(1.7)
 print('in_page',run('eval','JSON.stringify(window.__ffEvents)'),flush=True)
 (D/'dom-events.json').write_text(run('eval','JSON.stringify(window.__ffEvents)'))
 log('record_stop_request');print(run('record','stop'),flush=True);log('record_stop_return')
finally:
 try:run('close')
 except Exception:pass
 (D/'shell-events.json').write_text(json.dumps(events,ensure_ascii=False,indent=2))
