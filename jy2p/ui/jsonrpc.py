import json
from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer


from generic import GenericUI
from jy2p import util




def make_request_handler(router, rpc_class):

    rpc = rpc_class(router)

    class ReqestHandler(BaseHTTPRequestHandler):

        _acceptable_content_types = ['application/json']
        _required_keys = ['id', 'method', 'params']

        _jsonrpc_version = '1.0'

        _json_blank_response =  {'result' : None, 'error' : None, 'id' : None}
        _json_invalid_request = {'error' : -32600, 'id' : None}
        _json_parse_error = {'error' : -32700, 'id' : None}
        _json_no_such_method = {'error' : -32601, 'id' : None}
        _json_internal_error = {'error' : -32603, 'id' : None}
        
        def _parse_json(self):
            size = self.headers.getheader('Content-Length',0)
            try:
                size = int(size)
                if size > 0:
                    data = self.rfile.read(size)
                    self.json = json.loads(data)
                    return True
            except:
                self.send_error(400)
                
            
        def _check_keys(self):
            for k in self._required_keys:
                if k not in self.json:
                    return False
            return True

        def do_GET(self):
            self.send_error(400)

        def do_POST(self):
            if self.path == '/rpc':
                if self.headers.getheader('Content-Type','').lower() in self._acceptable_content_types:
                    if self._parse_json():
                        if self._check_keys():
                            j = dict(self._json_blank_response)
                            method = self.json['method']
                            params = self.json['params']
                            if rpc.has_method(method):
                                rpc_method = rpc.get_method(method)
                                try:
                                    if isinstance(params, dict):
                                        j['result'] = rpc_method(**params)
                                    elif isinstance(params, list):
                                        j['result'] = rpc_method(*params)
                                    else:
                                        raise Exception()
                                except Exception as e:
                                    self._log.error(e)
                                    j = dict(self._json_internal_error)
                            else:
                                j = dict(self._json_no_such_method)                                    
                            j['id'] = self.json['id']
                        else:
                            j = dict(self._json_invalid_request)
                    else:
                        j = dict(self._json_parse_error)
                    j['jsonrpc'] = self._jsonrpc_version
                    body = json.dumps(j)
                    self.send_response(200)
                    self.send_header('Content-Type',self._acceptable_content_types[0])
                    self.send_header('Content-Length', len(body))
                    self.end_headers()
                    self.wfile.write(body)
                    
            else:
                self.send_response(404,'NOT FOUND')

    util.inject_logger(ReqestHandler,'JsonRPC')
    return ReqestHandler

class JSONRPC:

    def __init__(self, router):
        self.router = router

    def has_method(self,method):
        return hasattr(self,'_rpc_'+method)
    
    def get_method(self,method):
        return getattr(self,'_rpc_'+method)

    def _rpc_kill(self, *args, **kwds):
        self.router.kill()
        return 1

    def _rpc_stop(self,*args, **kwds):
        self.router.stop()
        return 1

    def _rpc_start(self, *args, **kwds):
        self.router.start()
        return 1

    def _rpc_restart(self, *args, **kwds):
        self.router.restart()
        return 1

    def _rpc_start_time(self, *args, **kwds):
        return self.router.started_at()
        
    def _rpc_uptime(self, *args, **kwds):
        return self.router.uptime

    def _rpc_alive(self, *args, **kwds):
        return self.router.alive
        
    def _rpc_running(self, *args, **kwds):
        return self.router.running 

    def _rpc_status(self, *args, **kwds):
        return self.router.status

    def _rpc_network_status_code(self, *args, **kwds):
        return self.router.network_code
    
    def _rpc_network_status(self, *args, **kwds):
        return self.router.network

    def _rpc_active_peers(self, *args, **kwds):
        return self.router.context().commSystem().countActivePeers()

    def _rpc_bandwidth(self, *args, **kwds):
        recv, send = self.router.bandwidth
        return [int(recv), int(send)]

    def _rpc_get_participating_count(self, *args, **kwds):
        return self.router.context().tunnelManager().participatingCount
    
    def _rpc_get_tunnel_count(self, *args, **kwds):
        ls = []
        self.router.context().tunnelManager().listPools(ls)
        count = 0
        for pool in ls:
            count += len(pool.listTunnels())
        return count
        

class UI(GenericUI):

    def __init__(self,router, interface='127.0.0.1', port=7789):
        GenericUI.__init__(self,router)
        addr = (interface, port)
        self._server = HTTPServer(addr, make_request_handler(router, JSONRPC))

    def blocking_run(self):
        self._log.info('Router status: %s' % self.router.status)
        try:
            self._server.serve_forever()
        except Exception as e:
            self._log.error('Exception while running jsonrpc ui: %s' % e)
