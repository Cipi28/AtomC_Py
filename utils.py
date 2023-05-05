import sys

def err(fmt, *args):
    sys.stderr.write('error: ')
    sys.stderr.write(fmt % args)
    sys.stderr.write('\n')
    sys.exit(1)

def loadFile(filename):
    try:
        f = open(filename, "rb")
        buf = f.read()
        return buf.decode("utf-8")
    except IOError:
        err("cannot open file %s", filename)

