# -*- coding: utf-8 -*-
import pickle
import os

def getPolicy (filename="mypolicy_IAvsIA_100M_v4"):
    with open(filename, "rb") as file_handler:
        r = pickle.load(file_handler)
    return r
