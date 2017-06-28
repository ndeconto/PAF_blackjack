import pickle

## ne doit etre lance qu'avec python 2 !!!!

with open("temp.txt", "r") as f:
    exec("p = " + f.read())

print p

with open("policy_a_utilise_python2", "wb") as f:
    pickle.dump(p, f)
    
