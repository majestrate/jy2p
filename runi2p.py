#!/usr/bin/env jython
from jy2p.router import i2p_router
from jy2p.ui.jsonrpc import UI
import logging
import os

r = None

def main():
    global r
    fmt = '%(asctime)s\t-\t%(filename)s:%(lineno)-d\t-\t%(levelname)s\t%(name)s:\t%(message)s'
    logging.basicConfig(level=logging.INFO,format=fmt)
    r = i2p_router(os.environ['I2P'])
    UI(r).run()
    r.start()


if __name__ == '__main__':
    main()
