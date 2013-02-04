""" A standalone brainfuck interpreter/JIT compiler.
"""
import sys
from rpython.rlib.streamio import open_file_as_stream
from bf.jit import run

def main(argv):
    if len(argv) < 2:
        print __doc__
        return 1

    f = None
    bconly = argv[1] == "--print-bc-only"
    if bconly:
        f = open_file_as_stream(argv[2])
    else:
        f = open_file_as_stream(argv[1])
    data = f.readall()
    f.close()

    run(data, bconly)
    return 0

# -- Setup & Boilerplate -------------------------------------------------------

def target(driver, args):
    driver.exe_name = 'bf-%(backend)s'
    return main, None

def jitpolicy(driver):
    from rpython.jit.codewriter.policy import JitPolicy
    return JitPolicy()

if __name__ == '__main__':
    main(sys.argv)
