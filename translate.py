import util2
import util
def encode(inst):
    inst = inst.replace(',', '')
    for i in range(len(util.regs)): inst = inst.replace(util.regs[i], str(i))
    inst = inst.replace('$', '')
    inst = inst.split()
    out = util.ei
    if inst[0] in util.rwords:
        out = 0b000000 << 5
        if inst[0] == 'sll' or inst[0] == 'srl':
            try: rd, rt, shamt = [int(i, 0) for i in inst[1:]]
            except: return util.ea
            nrd, nrt, nshamt = rd & 0x1F, rt & 0x1F, shamt & 0x1F
            if [nrd, nrt, nshamt] != [rd, rt, shamt]: return util.ef
            rd, rt, shamt = nrd, nrt, nshamt
            out |= rt
            out <<= 5
            out |= rd
            out <<= 5
            out |= shamt
            out <<= 6
            out |= util.rwords[inst[0]]
        else:
            try: rd, rs, rt = [int(i, 0) for i in inst[1:]]
            except: return util.ea
            nrd, nrs, nrt = rd & 0x1F, rs & 0x1F, rt & 0x1F
            if [nrd, nrs, nrt] != [rd, rs, rt]: return util.ef
            rd, rs, rt = nrd, nrs, nrt
            out |= rs
            out <<= 5
            out |= rt
            out <<= 5
            out |= rd
            out <<= 11
            out |= util.rwords[inst[0]]
    elif inst[0] == 'lw' or inst[0] == 'sw':
        opcode = {'lw': 0b100011, 'sw': 0b101011}
        out = opcode[inst[0]] << 5
        try:
            inst[2] = inst[2].split('(')
            inst[2:] = inst[2][0], inst[2][1][:-1]
            rt, offset, rs = [int(i, 0) for i in inst[1:]]
        except: return util.ea
        nrt, nrs, noffset = rt & 0x1F, rs & 0x1F, offset & 0xFFFF
        if [nrt, nrs, noffset] != [rt, rs, offset]: return util.ef
        rt, rs, offset = nrt, nrs, noffset
        out |= rs
        out <<= 5
        out |= rt
        out <<= 16
        out |= offset
    elif inst[0] == 'beq':
        out = 0b000100 << 5
        try: rs, rt, offset = [int(i, 0) for i in inst[1:]]
        except: return util.ea
        nrs, nrt, noffset = rs & 0x1F, rt & 0x1F, offset & 0xFFFF
        if [nrs, nrt, noffset] != [rs, rt, offset]: return util.ef
        rs, rt, offset = nrs, nrt, noffset
        out |= rs
        out <<= 5
        out |= rt
        out <<= 16
        out |= offset
    elif inst[0] == 'addi':
        out = 0b001000 << 5
        try: rt, rs, imm = [int(i, 0) for i in inst[1:]]
        except: return util.ea
        nrt, nrs, nimm = rt & 0x1F, rs & 0x1F, imm & 0xFFFF
        if [nrt, nrs, nimm] != [rt, rs, imm]: return util.ef
        rt, rs, imm = nrt, nrs, nimm
        out |= rs
        out <<= 5
        out |= rt
        out <<= 16
        out |= imm
    return out
def decode(inst):
    inst = f'{inst:032b}'
    out = ''
    opcode = int(inst[0:6], 2)
    rs, rt = int(inst[6:11], 2), int(inst[11:16], 2)
    last16 = inst[16:32]
    if opcode == 0b000000:
        rd, aluOp = int(last16[0:5], 2), int(last16[10:16], 2)
        if aluOp == util.rwords['sll'] or aluOp == util.rwords['srl']:
            shamt = int(last16[5:10], 2)
            out = f'{util.rbins[aluOp]} {util.regs[rd]}, {util.regs[rt]}, {shamt}'
        else: out = f'{util.rbins[aluOp]} {util.regs[rd]}, {util.regs[rs]}, {util.regs[rt]}'
    elif opcode == 0b100011 or opcode == 0b101011:
        if opcode == 0b100011: out = 'lw'
        elif opcode == 0b101011: out = 'sw'
        out += f' {util.regs[rt]}, {int(last16, 2)}({util.regs[rs]})'
    elif opcode == 0b000100: out = f'beq {util.regs[rs]}, {util.regs[rt]}, {int(last16, 2)}'
    elif opcode == 0b001000: out = f'addi {util.regs[rt]}, {util.regs[rs]}, {int(last16, 2)}'
    return out