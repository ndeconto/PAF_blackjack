import pickle
import os

def getPolicy ():
    file_handler = open("mypolicy", "rb")
    return pickle.load(file_handler)