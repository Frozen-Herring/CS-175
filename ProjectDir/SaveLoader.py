'''
Created on May 21, 2017

@author: Justin Veyna
'''
try:
    from cPickle import Pickler, Unpickler
except ImportError:
    from pickle import Pickler, Unpickler

def pickle_save(obj, file_name):
    f = open(file_name, "wb")
    if f != None:
        p = Pickler(f, protocol=2)
        p.dump(obj)
        f.close()

def pickle_load(file_name):
    f = open(file_name, "rb")
    obj = None
    if f != None:
        u = Unpickler(f)
        obj = u.load()
        f.close()
    return obj

if __name__ == "__main__":
    obj = ["hello", "world"]
    pickle_save(obj, "test1.p")
    obj = pickle_load("test1.p")
    print(obj)