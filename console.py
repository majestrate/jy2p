import curses
import atexit
import time
import pyjsonrpc
import datetime

atexit.register(curses.endwin)
i2p = pyjsonrpc.HttpClient('http://127.0.0.1:7789/rpc')

mw = curses.initscr()

def now():
    return datetime.datetime.utcnow().strftime('%c')

def bw_str(v):
    if v > 1024:
        v /= 1024
        if v > 1024:
            return '%d MB/s' % v
        return '%d KB/s' % v
    return '%d B/s' % v
        

def paint():
    mw.clear()
    mw.border()
    up,down = tuple(i2p.bandwidth())
    status = i2p.status()
    net = i2p.network_status()
    peers = i2p.active_peers()
    participating = i2p.get_participating_count()
    tunnels = i2p.get_tunnel_count()
    uptime = i2p.uptime()
    top = 3
    
    mw.addstr(1,3, 'I2P Router Console')

    mw.addstr(top,3, 'Router: '+status)  
    mw.addstr(top, 30, 'Uptime: %d seconds' % int(uptime / 1000) )
    mw.addstr(top+1,3, 'Network: '+ net)
    
    ups = '=' * ( up / 1024 )

    dwns = '=' * ( down / 1024 )


    ratio = (participating / float(tunnels) ) if tunnels > 0 else 0
    ratios = '=' * int(ratio)

    mw.addstr(top+3,3,'Up')
    mw.addstr(top+4,3,bw_str(up))
    mw.addstr(top+3,9,ups)
    
    mw.addstr(top+6,3,'Down')
    mw.addstr(top+7,3,bw_str(down))
    mw.addstr(top+6,9,dwns)

    mw.addstr(top+9,3,'Peers: %d'%peers)
    mw.addstr(top+10,3,'Tunnels: %d'%tunnels)
    mw.addstr(top+12,3,'Participating Tunnels: %d'%participating)
    mw.addstr(top+13,3,('Share Ratio: %.2f ' % ratio)+ratios)


    mw.refresh()



def main():
    while True:
        paint()
        time.sleep(1)

if __name__ == '__main__':
    main()
