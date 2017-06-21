import pickle
import os

def getPolicy ():
    file_handler = open("mypolicy", "rb")
    pickle.load(file_handler)
    return policy