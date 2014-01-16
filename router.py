from net.i2p.router import Router
import util
import os

class i2p_router:
    
    def __init__(self,root_dir,props={}):
        util.inject_logger(self)
        self._config_path = os.path.join(root_dir,'router.config') 
        d = {
            'i2p.dir.config' : root_dir,
            'i2cp.disableInterface' : True
        }

        for k in props.iterkeys():
            d[k] = props[k]

        self._props = util.properties(d)

    def start(self):
        self._log.info('start:init')
        self._router = Router(self._config_path, self._props)
        self._log.info('start:run')
        self._router.runRouter()

