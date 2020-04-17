#!/usr/bin/expect
spawn cd ~/DABreceiver/welle.io
expect "~/DABreceiver/welle.io $"
send "mkdir build"
expect "~/DABreceiver/welle.io $"
send "cd build"
expect "~/DABreceiver/welle.io/build $"
send "cmake .. -DRTLSDR=1 -DBUILD_WELLE_IO=OFF"
expect "~/DABreceiver/welle.io/build $"
send "make"
expect "~/DABreceiver/welle.io/build $"
send "sudo make install"