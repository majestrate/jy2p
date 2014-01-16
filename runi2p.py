#!/usr/bin/env jython 
from router import i2p_router
import logging
import ui

def main():
    fmt = '%(asctime)s\t-\t%(filename)s:%(lineno)-d\t-\t%(levelname)s\t%(name)s:\t%(message)s'
    logging.basicConfig(level=logging.INFO,format=fmt)
    r = i2p_router()
    ui.LogUI(r).run()
    r.start()
  

if __name__ == '__main__':
    main()
