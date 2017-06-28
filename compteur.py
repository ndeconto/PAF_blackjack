def reset_total():
    with open('cmpt.txt', 'w') as file:
        file.write('0')

def read_total():
    with open('cmpt.txt','r') as file:
        line = file.readline()
        return(int(line))

def save_total(t):
    with open('cmpt.txt', 'w') as file:
        file.write(str(t))
