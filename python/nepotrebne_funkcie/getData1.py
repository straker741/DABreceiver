def getData1():
    frequency = getCenterFrequency()
    cmd = "sudo ~/rtl-dab/src/rtldab " + str(frequency)

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, shell=True)
    data = p.communicate()[1]
    wFile("rtldab_out.txt", data)
    pass
