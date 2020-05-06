#!/bin/bash

mkdir ~/DABreceiver/welle.io/build
cd ~/DABreceiver/welle.io/build && cmake ~/DABreceiver/welle.io -DRTLSDR=1 -DBUILD_WELLE_IO=OFF
cd ~/DABreceiver/welle.io/build && make
cd ~/DABreceiver/welle.io/build && sudo make install