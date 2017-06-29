def reset_total():
    with open('cmpt.txt', 'w') as file:
        file.write('0;0')

def read_total():
    try:
        with open('cmpt.txt','r') as file:
            line = file.readline().split(';')
            return(float(line[0]), int(float(line[1])))
    except (IOError):
        return 0, 0        #pas de fichier -> compteur a 0

def add_to_total(t):
    x, n = read_total()
    with open('cmpt.txt', 'w') as file:
        file.write(str(x + t)+';'+str(n+1))
