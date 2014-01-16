import util

class _generic_ui(object):
    
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
        util.fork(self.blocking_run)

class LogUI(_generic_ui):

    def blocking_run(self):
        util.inject_logger(self)
        while not self.router.running:
            self._log.info('Router running: %s' % self.router.running)
            self._log.info('Waiting for router to be running, Status: %s' % self.router.status)
            util.sleep(1)
        self._log.info('Router status: %s' % self.router.status)
        sleep_time = 1
        while self.router.running:
           bw = self.router.bandwidth(sleep_time)
           bw /= 1024 * 8.
           bw = int(bw)
           if bw > 0:
               self._log.info('bandwidth: %s KBps' % bw ) 
           util.sleep(sleep_time)
