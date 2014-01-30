#!/usr/bin/env bash

if [ "$I2P" == "" ] ; then
    I2P="$1"
fi

jp="$JYTHONPATH"
for jar in $I2P/libs/*.jar ; do
    jp="$jar:$jp"
done

JYTHONPATH="$jp" ./runi2p.py
