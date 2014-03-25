#!/usr/bin/env bash

jyopts=""
while getopts ":i" opt; do
    case $opt in
      i)
        jyopts="$jyopts -i"
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

jp="$JYTHONPATH"
for jar in $I2P/lib/*.jar ; do
    jp="$jar:$jp"
done

jyopts="$jyopts -J-Djava.library.path=${I2P}:${I2P}/lib"

JYTHONPATH="$jp" I2P="$I2P" jython $jyopts runi2p.py
