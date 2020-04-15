# Autor: Jakub Svajka
# Datum: 2.3.2020

import subprocess       # https://docs.python.org/2/library/subprocess.html

def rFile(path):
    """Read from a file."""
    try:
        with open(path, 'r') as f:    
            content = f.read()
        return content
    except:
        print("Error: Could not read from file.")
        return False
    pass

def extractStations(d):
    result = []
    for row in d:
        station = ""
        rowItems = row.split()[1:] # rozdeli riadok do listu a rovno uz ulozi do result ale bez cisel
        try:
            rowItems.remove("(current")
            rowItems.remove("station)")
        except ValueError:
            pass
        for item in rowItems:
            station += item
        result += station
    return result

def getStations():
    """NEFUNGUJE!"""
    command = "~/sdrbad*/sdrdab-cli -c 12C"
    p = subprocess.Popen(command, stdout=subprocess.PIPE, universal_newlines=True, shell=True)
    # communicate() vracia data v bytoch, ktore mozeme dekodovat: .decode('utf-8')
    # communicate() vracia data ako string ked predtym nastavime universal_newlines=True - potom odstranime /n /t a ine whitespaces
    p.communicate("list")
    data = p.communicate()[0].strip('\n')   # data je list riadkov
    p.kill()
    return extractStations(data)        # vracia zoznam stanic

def is_in(a, b):
    if b in a:
        return True
    return False
    pass

def getRadio(stanica):
    stations = getStations()
    # Mozeme zapisovat vsetky detaily o staniciach do databazy
    return is_in(stations, stanica)
    pass

def test1():
    p = subprocess.Popen(['cmd', '/C', "echo", "hello world"], stdout=subprocess.PIPE, universal_newlines=True)
    # communicate() vracia data v bytoch, ktore mozeme dekodovat: .decode('utf-8')
    # communicate() vracia data ako string ked predtym nastavime universal_newlines=True - potom odstranime /n /t a ine whitespaces
    data = p.communicate()[0].strip()
    print(data)
    p.kill()
    pass

def test2():
    #cmd1 = "~/sdrbad*/sdrdab-cli -c 12C"
    #cmd2 = "list"
    #command = "echo hi"

    #p1 = subprocess.Popen(cmd1, stdout=subprocess.PIPE, universal_newlines=True, shell=True)
    #p2 = subprocess.Popen(cmd2, stdout=subprocess.PIPE, stdin=p1.stdout, universal_newlines=True, shell=True)
    #p1.stdout.close()

    #p = subprocess.Popen(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines=True, shell=True)
    p = subprocess.Popen(stdout=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines=True, shell=True)
    pin = p.stdin
    pout = p.stdout
    pin.write("echo hi")
    #print(pout.read())
    data = p.communicate()[0]
    #p.communicate("list")
    #data = p.communicate()[0].strip('\n')   # data je list riadkov
    p.poll()
    p.wait()
    p.kill()
    print(data)
    pass

def string_to_2_procs_to_file(input_s, first_cmd, second_cmd, output_filename):
    """Example: string_to_2_procs_to_file('input data', ['awk', '-f', 'script.awk'], ['sort'], 'output.txt')"""
    with open(output_filename, 'wb') as out_f:
        p2 = subprocess.Popen(second_cmd, stdin=PIPE, stdout=out_f)
        p1 = subprocess.Popen(first_cmd, stdout=p2.stdin, stdin=PIPE)
        p1.communicate(input=bytes(input_s))
        p1.wait()
        p2.stdin.close()
        p2.wait()
    pass

if __name__ == "__main__":
    

    pass