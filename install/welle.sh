#!/bin/bash

mkdir $HOME/DABreceiver/welle.io/build
cd $HOME/DABreceiver/welle.io/build && cmake $HOME/DABreceiver/welle.io -DRTLSDR=1 -DBUILD_WELLE_IO=OFF
cd $HOME/DABreceiver/welle.io/build && make
cd $HOME/DABreceiver/welle.io/build && sudo make install