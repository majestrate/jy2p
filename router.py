from net.i2p.router import Router
import util
import os

class i2p_router:
    
    def __init__(self,root_dir=None,props={}):
        util.inject_logger(self)
        if root_dir is None:
            root_dir = os.path.join(os.environ['HOME'],'.i2p')

        self._router_status = 'Initialize'
        self._load_config(root_dir,props)

    def bandwidth(self,sec=1):
        if not isinstance(sec,int):
            sec = int(sec)
        if sec >= 300:
            return self._router.get5mRate()
        elif sec >= 60:
            return self._router.get1mRate()
        elif sec >= 15:
            return self._router.get15sRate()
        if sec >= 1:
            return self._router.get1sRate()

    @property
    def status(self):
        return self._get_status()

    def _status(self,status):
        self._router_status = str(status)
        self._log.info('Status: '+self._router_status)

    def _get_status(self):
        return self._router_status

    @property
    def alive(self):
        return self._router.isAlive()
    
    @property
    def running(self):
        return self.status == 'Running'

    @property
    def done(self):
        return self.status == 'Done'
    
    def _wait_for_stop(self):
        self._wait(lambda : self.alive)
        self._status('Done')

    def _wait_for_alive(self):
        self._wait(lambda : not self.alive)
        self._status('Running')
        
    def _wait(self,hook):
        while hook():
            util.sleep()

    def _load_config(self,root_dir,props):
        self._status('LoadConfig')
        self._config_path = os.path.join(root_dir,'router.config') 
        d = {
            'i2p.dir.config' : root_dir,
            'i2cp.disableInterface' : True
        }

        for k in props.iterkeys():
            d[k] = props[k]

        self._props = util.properties(d)

    def start(self):
        self._status('Starting')
        self._router = Router(self._config_path, self._props)
        util.fork(self._router.runRouter)
        self._wait_for_alive()

    def blocking_kill(self):
        if self.status == 'Running':
            self._router.shutdown(Router.EXIT_HARD)
            self._wait_for_stop()
    
    def kill(self):
        util.fork(self.blocking_kill)

    def cancel_stop(self):
        if self._router.gracefulShutdownInProgress():
            self._router.cancelGracefulShutdown()
            self._status('Running')

    def blocking_stop(self):
        self._router.shutdownGracefully()
        self._status('GracefulStop')
        self._wait_for_stop()
        
    def stop(self):
        util.fork(self.blocking_stop)


    def blocking_restart(self):
        if self._status == 'Running':
            self._status('Restarting')
            self._router.restart()
            self._wait_for_alive()

    def restart(self):
        util.fork(self.blocking_restart)

