import pickle
import os

def getPolicy ():
    file_handler = open("mypolicy", "r")
    pickle.load(file_handler)
    return policy