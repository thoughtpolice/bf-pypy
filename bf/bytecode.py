bytecodes = [ 'INCT'
            , 'PUTV'
            , 'GETV'
            , 'MOVT'
            , 'LOOP'
            , 'GOTO'
            ]
for i, bc in enumerate(bytecodes):
    globals()[bc] = i

def dumpl(i, code, cmap):
    bc  = bytecodes[ord(code[i])]
    inp = cmap[i]
    if inp == 0:
        return ("%d:\t%s" % (i, bc))
    else:
        return ("%d:\t%s %d" % (i, bc, inp))


class ByteCode(object):
    _immutable_fields_ = [ 'code', 'codemap[*]' ]

    def __init__(self, code, cmap):
        self.code    = code
        self.codemap = cmap

    def dump(self):
        lines, i = [], 0
        for i in range(0, len(self.code)):
            lines.append(dumpl(i, self.code, self.codemap))
        return '\n'.join(lines)
