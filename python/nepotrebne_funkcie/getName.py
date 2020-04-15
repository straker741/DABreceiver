import os
import subprocess
import time

def getName():
    stream = os.popen('lsusb | grep "Semiconductor"')
    output = stream.read()
    return output
    pass

def run_cmd(cmd):
    cmd = cmd.split(' ')
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    return result.stdout.decode('utf-8').split('\n'), result.stderr.decode('utf-8').split('\n')
    pass

def print_run_cmd():
    output, err = run_cmd('ls')

    for line in output:
        print(line)
    pass

def getName2(cmd):
    # NEFUNGUJE LEBO VRATI NIC KED SA NESKONCI PO 5 SEKUNDACH
    cmd = cmd.split(' ')
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        outs, errs = proc.communicate(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()
        outs, errs = proc.communicate()
    return outs, errs

def getName3(cmd):
    cmd = cmd.split(' ')
    outputFile = open('out.txt', 'w')
    with subprocess.Popen(cmd, stdout=outputFile, stderr=outputFile, universal_newlines=True) as proc:
        try:
            proc.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.communicate()

    outputFile.close()

    with open("out.txt", 'r') as f:
        data = f.read()
    return data
    pass


def getName4(cmd):
    cmd = cmd.split(' ')
    with open('out.txt', 'w') as outputFile:
        try:
            output = subprocess.check_output(cmd, timeout=5)
            outputFile.write(output)
        except subprocess.TimeoutExpired:
            outputFile.write(output)

    with open("out.txt", 'r') as f:
        data = f.read()
    return data
    pass

def getName5(cmd):
    cmd = cmd.split(' ')
    output = []
    print("Start!")
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True) as p:
        print("Opened!")
        while p.poll() is None:
            line = p.stdout.readline()
            print(line)
    return 0
    pass

def getName6(cmd):
    cmd = cmd.split(' ')
    print("Started!")
    outs = ""
    errs = ""
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True) as p:
        print("Opened!")
        try:
            outs, errs = p.communicate()           
        except subprocess.TimeoutExpired as e:
            p.terminate()
            p.wait()
            print("Expired!", e.stdout, e.stderr)         
    print("Returning!")
    return outs, errs
    pass

    #return output
#print(getName())
#print_run_cmd()

#out, err = getName2('python3 /var/www/html/python/add_wait.py')
#print(out)

#print(getName5('python3 /var/www/html/python/add_wait.py'))
print(getName6('timeout 5 python3 /var/www/html/python/add_wait.py'))