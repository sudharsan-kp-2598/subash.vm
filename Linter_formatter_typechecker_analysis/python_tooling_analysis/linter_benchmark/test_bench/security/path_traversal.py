import os

def read_file(name):
    return open(os.path.join("/safe/base", name)).read()
