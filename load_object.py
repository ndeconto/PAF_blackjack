# -*- coding: utf-8 -*-
import pickle
import os

def getPolicy ():
    with open("mypolicy_IAvsIA_50M_v2", "rb") as file_handler:
        r = pickle.load(file_handler)
    return r
