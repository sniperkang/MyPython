def find_start_imooc(fname):
    f = open(fname)
    for line in f:
        if line.startswith('imooc'):
            print line

def find_in_imooc(fname):
    f = open(fname)
    for line in f:
        if line.startswith('imooc')\
                and line[:-1].endswith('imooc'):
            print line

a = '_value1'

a and (a[0]=='_' or 'a' <= a[0] <= 'z')