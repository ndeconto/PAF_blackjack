import pickle

def getPolicy ():
    file_handler = open("mypolicy", "r")
    pickle.load(policy,file_handler)
    return policy