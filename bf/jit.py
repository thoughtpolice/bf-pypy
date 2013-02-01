import os
from rpython.rlib import jit

from bf        import bytecode
from bf.parser import parse

# -----------------------------------------------------------------------------
# -- Interpreter --------------------------------------------------------------

def get_location(pc, bc, bcode):
    lines, i, x = [], 0, 0
    # Append regular instruction
    line = "["+bytecode.dumpl(pc, bcode.code, bcode.codemap)+"]"
    lines.append(line)

    return "; ".join(lines)

jitdriver = jit.JitDriver(greens=['pc', 'bc', 'bcode'],
                          reds='auto',
                          get_printable_location = get_location
                          )

@jit.elidable
def get_matching_codemap(bc, pc): return bc.codemap[pc]
@jit.elidable
def get_matching_code(bc, pc): return bc.code[pc]

def interpret(bcode):
    pc   = 0
    bc   = ord(get_matching_code(bcode, pc))
    tape = [0] * 30000
    pos  = 0

    while pc < len(bcode.code):
        jitdriver.jit_merge_point(pc=pc, bc=bc, bcode=bcode)
        bc = ord(get_matching_code(bcode, pc))

        # Simple cases
        if   bc == bytecode.INCT:
            tape[pos] += get_matching_codemap(bcode, pc)
        elif bc == bytecode.MOVT:
            pos += get_matching_codemap(bcode, pc)
            diff = pos - len(tape)
            if diff >= 0:
                tape.extend([0 for _ in range(0,diff)])
        elif bc == bytecode.PUTV:
            os.write(1, chr(tape[pos]))
        elif bc == bytecode.GETV:
            tape[pos] = ord(os.read(1, 1)[0])
        # Loop case
        elif bc == bytecode.LOOP and tape[pos] == 0:
            pc = get_matching_codemap(bcode, pc)
        elif bc == bytecode.GOTO and tape[pos] != 0:
            pc = get_matching_codemap(bcode, pc)

        pc += 1

# -----------------------------------------------------------------------------
# -- Driver -------------------------------------------------------------------

def run(data, print_bc):
    if print_bc:
        print parse(data).dump()
    else:
        interpret(parse(data))
