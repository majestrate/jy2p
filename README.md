## Jy2P -- Jython I2P Wrapper

### Dependancies

* Jython 2.7 ( http://jython.org/downloads.html )
* I2P ( https://geti2p.net/download )

### To Run

    git clone https://github.com/majestrate/jy2p/
    cd jy2p
    ./jy2p.sh [OPTION]... /path/to/i2p/installation/directory/

#### Options

* `-i` Open the Jython interpreter after starting the router. The router will
  be accessible via the `r` variable. The interpreter will close when the
  router shuts down.
* `-p` Add libraries from the local Python 2 installation to the Jython path.
  Libraries in the `dist-packages` and `site-packages` folders are added.
