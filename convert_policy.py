from load_object import getPolicy


from os import system
from sys import argv

p  = getPolicy(argv[1])

with open("temp.txt", "w") as f:
    f.write(p.__repr__())

system("C:/Python27/python convert_policy_python_2.py " + argv[1])

