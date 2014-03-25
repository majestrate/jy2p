#!/usr/bin/env bash

jp=""
jyopts=""
while getopts ":ip" opt; do
    case $opt in
      i)
        jyopts="$jyopts -i"
        ;;
      p)
        jp=$(python2 -c 'import sys; print(":".join([x for x in sys.path if "dist-packages" in x or "site-packages" in x]))')
        ;;
      \?)
        echo "Invalid option: -$OPTARG" >&2
        ;;
    esac
done
shift $((OPTIND-1))

if [ "$I2P" == "" ] ; then
    I2P="$1"
fi

if [ "$I2P" == "" ] ; then
    echo "An I2P installation dir must be provided."
    echo "Usage: ./jy2p.sh [OPTION]... [I2PDIR]"
    echo "Alternatively, you can set the I2P environment variable."
    exit 2
fi

cp=""
for jar in $I2P/lib/*.jar ; do
    cp="$jar:$cp"
done

jyopts="$jyopts -J-cp $cp"
jyopts="$jyopts -J-Djava.library.path=${I2P}:${I2P}/lib"

JYTHONPATH="$JYTHONPATH:$jp" I2P="$I2P" jython $jyopts runi2p.py
