def rFile(path):
    """Reading from a file."""
    try:
        with open(path, 'r') as f:    
            content = f.read()
        return content
    except:
        print("Error: Could not read from file.")
        return '-1'
    pass

def convertListToStr(l):
    name = l[0]
    for i in range(1, len(l)):
        name += ' ' + l[i]
    return name
    
def najdiStanice(p):
    z = rFile(p).split('\n')
    for i in range(len(z)):
        if z[i] == 'Service list':
            z = z[i+1 : i+11]
            break
    else:
        # nepodarilo sa najst 'Service list\n'
        return False
    return z
    pass

def extractNames(z):
    pocetProgramov = 10
    result = []
    for row in z:
        row = row.split()
        row = row[1:-10]
        name = convertListToStr(row)       
        result.append(name)   
    return result
    pass

def testName(a, b):
    if b in a:
        return True
    return False
    pass

def getRadio(path, stanica):
    zoznam = najdiStanice(path)
    # Mozeme zapisovat vsetky detaily o staniciach do databazy
    zoznamNazvovStanic = extractNames(zoznam)
    return testName(zoznamNazvovStanic, stanica)