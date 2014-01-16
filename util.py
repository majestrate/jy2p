from functools import wraps
from java.util import Properties
import logging
import time
import threading

def inject_logger(obj):
    """
    inject a logger into an object 
    """
    obj._log = logging.getLogger(obj.__class__.__name__)
    return obj

def properties(props_dict):
    """
    make a java.util.Properties from a python dict
    """
    p = Properties()
    for k in props_dict.iterkeys():
        v = props_dict[k]
        if isinstance(v,bool):
            if v:
                v = 'true'
            else:
                v = 'false'
        p.put(k,v)
    return p

def sleep(n=.25):
    """
    Wrapper for time.sleep
    """
    time.sleep(n)

def fork(*args):
    """
    fork off a function to background
    """
    func = args[0]
    if len(args) > 1:
        args = tuple(args[1:])
        threading.Thread(target=func,args=args).start()
    else:
        threading.Thread(target=func).start()
        
