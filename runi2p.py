#!/usr/bin/env jython 
from router import i2p_router
import logging

def main():
    logging.basicConfig(level=logging.INFO)
    r = i2p_router('/tmp/i2p')
    r.start()
  

if __name__ == '__main__':
    main()
