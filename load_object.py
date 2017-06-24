# -*- coding: utf-8 -*-
import pickle
import os

def getPolicy ():
    file_handler = open("mypolicy_11M", "rb")
    return pickle.load(file_handler)
