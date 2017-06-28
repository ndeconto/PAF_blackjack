from load_object import getPolicy


from os import system

p  = getPolicy("mypolicy_100M")

with open("temp.txt", "w") as f:
    f.write(p.__repr__())

system("C:/Python27/python convert_policy_python_2.py")

