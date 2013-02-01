from bf import bytecode

# ------------------------------------------------------------------------------
# -- Parser --------------------------------------------------------------------

def parse(program):
    bc, codemap, loopmap, pc = [], [], [], 0

    ## Loop state
    # Used for constant folding
    cinc, cfold1 = 0, False # This corresponds to +/-
    cmov, cfold2 = 0, False # This corresponds to >/<

    for char in program:
        # Constant folding case
        if char == '+' or char == '-':
            if cfold2:
                if cmov != 0:
                    bc.append(chr(bytecode.MOVT))
                    codemap.append(cmov)
                    pc += 1
                cmov, cfold2   = 0, False
            cfold1 = True
            cinc  = (cinc+1) if char == '+' else (cinc-1)

        # Constant folding case
        elif char == '<' or char == '>':
            if cfold1:
                if cinc != 0:
                    bc.append(chr(bytecode.INCT))
                    codemap.append(cinc)
                    pc += 1
                cinc, cfold1   = 0, False
            cfold2 = True
            cmov   = (cmov+1) if char == '>' else (cmov-1)

        # Loop bodies
        elif char == '[':
            if cfold1: # If we were folding something else...
                if cinc != 0:
                    bc.append(chr(bytecode.INCT))
                    codemap.append(cinc)
                    pc += 1
                cinc, cfold1   = 0, False
            elif cfold2: # If we were folding something else...
                if cmov != 0:
                    bc.append(chr(bytecode.MOVT))
                    codemap.append(cmov)
                    pc += 1
                cmov, cfold2   = 0, False

            loopmap.append(pc)
            codemap.append(pc)
            bc.append(chr(bytecode.LOOP))
            pc += 1
        elif char == ']':
            if cfold1: # If we were folding something else...
                if cinc != 0:
                    bc.append(chr(bytecode.INCT))
                    codemap.append(cinc)
                    pc += 1
                cinc, cfold1   = 0, False
            elif cfold2: # If we were folding something else...
                if cmov != 0:
                    bc.append(chr(bytecode.MOVT))
                    codemap.append(cmov)
                    pc += 1
                cmov, cfold2   = 0, False

            bc.append(chr(bytecode.GOTO))
            point = loopmap.pop()
            codemap[point] = pc
            codemap.append(point)
            pc += 1

        # Trivial cases
        elif char == ',':
            if cfold1: # If we were folding something else...
                if cinc != 0:
                    bc.append(chr(bytecode.INCT))
                    codemap.append(cinc)
                    pc += 1
                cinc, cfold1   = 0, False
            elif cfold2: # If we were folding something else...
                if cmov != 0:
                    bc.append(chr(bytecode.MOVT))
                    codemap.append(cmov)
                    pc +=1
                cmov, cfold2   = 0, False

            bc.append(chr(bytecode.GETV))
            codemap.append(0)
            pc += 1

        elif char == '.':
            if cfold1: # If we were folding something else...
                if cinc != 0:
                    bc.append(chr(bytecode.INCT))
                    codemap.append(cinc)
                    pc += 1
                cinc, cfold1   = 0, False
            elif cfold2: # If we were folding something else...
                if cmov != 0:
                    bc.append(chr(bytecode.MOVT))
                    codemap.append(cmov)
                    pc += 1
                cmov, cfold2   = 0, False

            bc.append(chr(bytecode.PUTV))
            codemap.append(0)
            pc += 1

    # Handle dangling constants
    if cinc != 0:
        bc.append(chr(bytecode.INCT))
        codemap.append(cinc)
    if cmov != 0:
        bc.append(chr(bytecode.MOVT))
        codemap.append(cmov)

    return bytecode.ByteCode("".join(bc), codemap[:])
