import subprocess,time,json,pathlib
D=pathlib.Path('/tmp/frameforge-ff14-20261123');D.mkdir(exist_ok=True)
base=['npx','--yes','--package','agent-browser@0.43.0','agent-browser','--session','frameforge-newrec']
def run(*args):
 p=subprocess.run(base+list(args),capture_output=True,text=True,timeout=60)
 if p.returncode:raise RuntimeError(f'{args} {p.stderr}')
 return p.stdout.strip()
try:
 print(run('open','https://todomvc.com/examples/react/dist/'),flush=True)
 run('eval','localStorage.clear();location.reload()')
 print(run('record','start',str(D/'recording.webm'),'--fps','30','--contact-sheet'),flush=True)
 time.sleep(1)
 t=time.monotonic()
 run('fill','input.new-todo','Première tâche');run('press','Enter')
 print('first',run('eval',"JSON.stringify([...document.querySelectorAll('ul.todo-list li')].map(x=>x.innerText))"),flush=True)
 time.sleep(1)
 run('fill','input.new-todo','Deuxième tâche');run('press','Enter')
 print('second',run('eval',"JSON.stringify([...document.querySelectorAll('ul.todo-list li')].map(x=>x.innerText))"),flush=True)
 time.sleep(1)
 run('click','ul.todo-list li:first-child input.toggle')
 print('third',run('eval',"JSON.stringify([...document.querySelectorAll('ul.todo-list li')].map(x=>({text:x.innerText,done:x.classList.contains('completed')})))"),flush=True)
 time.sleep(1)
 print('wall_since_actions',round(time.monotonic()-t,3),flush=True)
 print('stop',run('record','stop'),flush=True)
finally:
 try:run('close')
 except Exception:pass
