# -*- coding: utf-8 -*-
import pickle
import os

def getPolicy ():
    with open("mypolicy_IAvsIA-50M_v1_bon_res", "rb") as file_handler:
        r = pickle.load(file_handler)
    return r
