import subprocess,time,json,pathlib,datetime
D=pathlib.Path('/tmp/frameforge-ff07-20261123');D.mkdir(exist_ok=True)
events=[]
def run(*args):
 p=subprocess.run(['agent-browser','--session','frameforge-v3',*args],capture_output=True,text=True,timeout=40)
 if p.returncode:raise RuntimeError(f'{args}: {p.stderr}')
 return p.stdout.strip()
def log(name,**kw):
 events.append(dict(event=name,mono_ns=time.monotonic_ns(),utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),**kw))
try:
 run('open','https://todomvc.com/examples/react/dist/')
 run('eval',"localStorage.clear();location.reload()")
 log('record_start_request')
 print(run('record','start',str(D/'capture.webm')),flush=True)
 log('record_start_return')
 run('eval',"(()=>{let x=document.createElement('div');x.id='ff-sync';x.textContent='SYNC';x.style='position:fixed;top:0;left:0;width:100%;height:90px;background:#f00;color:white;font-size:60px;z-index:2147483647;text-align:center';document.body.append(x)})()")
 time.sleep(0.8)
 log('sync_flash_request')
 run('eval',"document.querySelector('#ff-sync').style.background='#00ff00'")
 log('sync_flash_return')
 time.sleep(0.8)
 run('eval',"document.querySelector('#ff-sync').remove()")
 time.sleep(0.5)
 for i,(label,action) in enumerate([('Première tâche','add'),('Deuxième tâche','add'),('Première tâche','complete')]):
  log('action_begin',index=i+1,action=action,label=label)
  if action=='add':
   run('fill','input.new-todo',label)
   run('press','Enter')
  else:
   run('click','ul.todo-list li:first-child input.toggle')
  log('action_command_return',index=i+1)
  state=run('eval',"JSON.stringify([...document.querySelectorAll('ul.todo-list li')].map(x=>({text:x.innerText,done:x.classList.contains('completed')})))")
  log('dom_assertion',index=i+1,state=state)
  print(i+1,state,flush=True)
  time.sleep(4)
 log('record_stop_request')
 print(run('record','stop'),flush=True)
 log('record_stop_return')
finally:
 try:run('close')
 except Exception:pass
 (D/'events.json').write_text(json.dumps(events,ensure_ascii=False,indent=2))
 print('events',len(events),flush=True)
