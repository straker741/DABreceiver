#!/bin/bash

cd ~/DABreceiver/welle.io
mkdir build
cd build
cmake .. -DRTLSDR=1 -DBUILD_WELLE_IO=OFF
make
sudo make install