#!/usr/bin/expect
spawn cd ~/DABreceiver/welle.io
expect "pi@raspberrypi:~/DABreceiver/welle.io $"
send "mkdir build"
expect "pi@raspberrypi:~/DABreceiver/welle.io $"
send "cd build"
expect "pi@raspberrypi:~/DABreceiver/welle.io/build $"
send "cmake .. -DRTLSDR=1 -DBUILD_WELLE_IO=OFF"
expect "pi@raspberrypi:~/DABreceiver/welle.io/build $"
send "make"
expect "pi@raspberrypi:~/DABreceiver/welle.io/build $"
send "sudo make install"