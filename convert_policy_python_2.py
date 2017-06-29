import pickle
from sys import argv
## ne doit etre lance qu'avec python 2 !!!!

with open("temp.txt", "r") as f:
    exec("p = " + f.read())

print p

with open("policy_pour_python2/" + argv[1] + "_PYTHON2", "wb") as f:
    pickle.dump(p, f)
    
