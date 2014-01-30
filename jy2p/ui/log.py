from generic import GenericUI
        
        
class UI(GenericUI):

    def blocking_run(self):
        self.wait_for_router()
        self._log.info('Router status: %s' % self.router.status)
        net_status = None
        while self.router.running:
            i,o = self.router.bandwidth()
            iunit, ounit = 'B', 'B'
            if i > 1024:
                i /= 1024
                iunit = 'KB'
                if i > 1024:
                    i /= 1024
                    iunit = 'MB'
            if o > 1024:
                o /= 1024
                ounit = 'KB'
                if o > 1024:
                    o /= 1024
                    ounit = 'MB'
            self._log.info('Bandwidth: %d %sps | %d %sps' % ( i,iunit, o, ounit) )
            new_net_status = self.router.network
            if new_net_status != net_status:
                net_status = new_net_status
                self._log.info('Network: '+net_status)
            util.sleep(1)


