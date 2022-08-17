import os

def Founds():
    try:
        os.stat('networkcredentials.txt')
        return True
    except OSError:
        return False  

def Clear():
    os.remove("networkcredentials.txt")

def Save(n,p):
    f = open('networkcredentials.txt', 'w')
    f.write(n)
    f.write('\n')
    f.write(p)
    f.write('\n')
    f.close();

def Read():
    f = open('networkcredentials.txt', 'r')
    lines = f.readlines()
    f.close();
    return lines
