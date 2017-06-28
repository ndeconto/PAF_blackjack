# -*- coding: utf-8 -*-
import pickle
import os

def getPolicy ():
    with open("mypolicy_vsBank", "rb") as file_handler:
        r = pickle.load(file_handler)
    return r
