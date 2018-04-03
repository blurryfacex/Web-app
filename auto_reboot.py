import os,time,sys,subprocess

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def log(s):
    print ('[Monitor] %s' %s)

class MyFileSystemEventHandler(FileSystemEventHandler):
    def __init__(self,fn):
        super(FileSystemEventHandler).__init__()
        self.restart=fn
    def on_any_event(self,event):
        if event.src_path.endswith('.py'):
            log('Python source file changed: %s' %event.src_path)
            self.restart()

command=['echo','ok']
process=None

def kill_process():
    global process
    if process:
        log('Kill Process [%s]' %process.pid)
        process.kill()
        process.wait()
        log('Process ended with code %s' %process.returncode)
        process=None

def start_process():
    global process,command
    log('Start process [%s]' %' '.join(command))
    process=subprocess.Popen(command,stdin=sys.stdin,stdout=sys.stdout,stderr=sys.stderr)

def restart_process():
    kill_process()
    start_process()

def start_watch(path,callback):
    observer=Observer()
    observer.schedule(MyFileSystemEventHandler(restart_process),path,recursive=True)
    observer.start()
    log('Watching directory %s...' %path)
    start_process()
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__=='__main__':
    abspath = os.path.abspath('.')
    argv=sys.argv[1:]
    if not argv:
        argv=['{0}\\auto_reboot.py {1}\\www\\app.py'.format(abspath,abspath)]
    if argv[0]!='python':
        argv.insert(0,'python')
    command=argv
    print ('d',os.path.abspath('.'))
    start_watch(abspath,None)