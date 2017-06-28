# -*- coding: utf-8 -*-
import pickle
import os

def getPolicy (filename="mypolicy_100M"):
    with open(filename, "rb") as file_handler:
        r = pickle.load(file_handler)
    return r
