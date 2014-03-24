## Jy2P -- (Toy) Jython I2P Wrapper

### Dependancies

* Jython 2.7 ( http://jython.org/downloads.html )
* I2P ( https://geti2p.net/download )

### To Run

    git clone https://github.com/majestrate/jy2p/
    cd jy2p
    ./jy2p.sh /path/to/i2p/installation/directory/

To open the Jython interpreter after starting the router:

    ./jy2p.sh -i /path/to/i2p/installation/directory/

The router will be accessible via the `r` variable. The interpreter will close
when the router shuts down.
