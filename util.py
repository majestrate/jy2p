from functools import wraps
from java.util import Properties
import logging

def inject_logger(obj):
    """
    inject a logger into an object 
    """
    obj._log = logging.getLogger(obj.__class__.__name__)
    return obj

def properties(props_dict):
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
