from jy2p import util

class GenericUI(object):
    
    def __init__(self,router):
        self.router = router

    def router_restart(self):
        self.router.restart()
        return self.router.status

    def router_alive(self):
        return self.router.alive

    def router_status(self):
        return self.router.status
        
    def blocking_run(self):
        pass

    def run(self):
        util.inject_logger(self)
        util.fork(self.blocking_run)

    def wait_for_router(self):
        while not self.router.running:
            self._log.info('Router running: %s' % self.router.running)
            self._log.info('Waiting for router to be running, Status: %s' % self.router.status)
            util.sleep(1)
