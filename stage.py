import util2, util
ctrl = {0b000000: (0b1, 0b0, 0b0, 0b1, 0b0, 0b0, 0b0, 0b10), 0b100011: (0b0, 0b1, 0b1, 0b1, 0b1, 0b0, 0b0, 0b00), 0b101011: (0b0, 0b1, 0b0, 0b0, 0b0, 0b1, 0b0, 0b00), 0b000100: (0b0, 0b0, 0b0, 0b0, 0b0, 0b0, 0b1, 0b01), 0b001000: (0b0, 0b1, 0b0, 0b1, 0b0, 0b0, 0b0, 0b00)}
def EX_fwd():
    if util2.mwc['REG_WRITE'] == 1 and util2.mw['RD'] != 0 and util2.mw['RD'] == util2.dx['RS'] and (util2.xm['RD'] != util2.dx['RS'] or util2.xmc['REG_WRITE'] == 0): util2.fwd['FWD_A'] = 1
    elif util2.xmc['REG_WRITE'] == 1 and util2.xm['RD'] != 0 and util2.xm['RD'] == util2.dx['RS']: util2.fwd['FWD_A'] = 2
    else: util2.fwd['FWD_A'] = 0
    if util2.mwc['REG_WRITE'] == 1 and util2.mw['RD'] != 0 and util2.mw['RD'] == util2.dx['RT'] and (util2.xm['RD'] != util2.dx['RT'] or util2.xmc['REG_WRITE'] == 0): util2.fwd['FWD_B'] = 1
    elif util2.xmc['REG_WRITE'] == 1 and util2.xm['RD'] != 0 and util2.xm['RD'] == util2.dx['RT']: util2.fwd['FWD_B'] = 2
    else: util2.fwd['FWD_B'] = 0
    if util2.fwd['FWD_A'] == 0 or not util.data_hzd: util.outFwdA = util2.dx['A']
    elif util2.fwd['FWD_A'] == 1:
        if util2.mwc['MEM_TO_REG'] == 1: util.outFwdA = util2.mw['LMD']
        else: util.outFwdA = util2.mw['ALU_OUT']
    elif util2.fwd['FWD_A'] == 2: util.outFwdA = util2.xm['ALU_OUT']
    if util2.fwd['FWD_B'] == 0 or not util.data_hzd: util.outFwdB = util2.dx['B']
    elif util2.fwd['FWD_B'] == 1:
        if util2.mwc['MEM_TO_REG'] == 1: util.outFwdB = util2.mw['LMD']
        else: util.outFwdB = util2.mw['ALU_OUT']
    elif util2.fwd['FWD_B'] == 2: util.outFwdB = util2.xm['ALU_OUT']
def ID_hzd():
    if_id_rs = (util2.fd['IR'] & 0x03E00000) >> 21
    if_id_rt = (util2.fd['IR'] & 0x001F0000) >> 16
    if util2.dxc['MEM_READ'] == 1 and (util2.dx['RT'] == if_id_rs or util2.dx['RT'] == if_id_rt) and util.data_hzd:
        util2.fwd['PC_WRITE'] = 0
        util2.fwd['fd_WRITE'] = 0
        util2.fwd['STALL'] = 1
    elif (util2.dxc['BRANCH'] == 1 or util2.xmc['BRANCH'] == 1) and util.ctrl_hzd:
        util2.fwd['fd_WRITE'] = 0
        util2.fwd['STALL'] = 1
    else:
        util2.fwd['PC_WRITE'] = 1
        util2.fwd['fd_WRITE'] = 1
        util2.fwd['STALL'] = 0
def IF():
    try: curInst = util2.inst[util2.pc//4]
    except IndexError: curInst = 0
    util.ran['IF'] = (0, 0) if util2.fwd['STALL'] == 1 else (util2.pc//4, curInst)
    util.idle['IF'] = (util2.fwd['STALL'] == 1)
    if util2.fwd['IF_ID_WRITE'] == 1 or not util.data_hzd:
        util2.fd['NPC'] = util2.pc + 4
        util2.fd['IR'] = curInst
    if util2.fwd['PC_WRITE'] == 1 or not util.data_hzd:
        if util2.xm['ZERO'] == 1 and util2.xmc['BRANCH'] == 1: util2.pc = util2.xm['BR_TGT']
        elif util2.fwd['STALL'] != 1: util2.pc = util2.pc + 4
def ID():
    util.ran['ID'] = (0, 0) if util2.fwd['STALL'] == 1 else util.ran['IF']
    util.idle['ID'] = (util2.fwd['STALL'] == 1)
    if util2.fwd['STALL'] == 1:
        util2.dxc['REG_DST'] = 0
        util2.dxc['ALU_SRC'] = 0
        util2.dxc['MEM_TO_REG'] = 0
        util2.dxc['REG_WRITE'] = 0
        util2.dxc['MEM_READ'] = 0
        util2.dxc['MEM_WRITE'] = 0
        util2.dxc['BRANCH'] = 0
        util2.dxc['ALU_OP'] = 0
    else:
        opcode = (util2.fd['IR'] & 0xFC000000) >> 26
        util2.dxc['REG_DST'] = ctrl[opcode][0]
        util2.dxc['ALU_SRC'] = ctrl[opcode][1]
        util2.dxc['MEM_TO_REG'] = ctrl[opcode][2]
        util2.dxc['REG_WRITE'] = ctrl[opcode][3]
        util2.dxc['MEM_READ'] = ctrl[opcode][4]
        util2.dxc['MEM_WRITE'] = ctrl[opcode][5]
        util2.dxc['BRANCH'] = ctrl[opcode][6]
        util2.dxc['ALU_OP'] = ctrl[opcode][7]
    util2.dx['NPC'] = util2.fd['NPC']
    reg1 = (util2.fd['IR'] & 0x03E00000) >> 21
    util2.dx['A'] = util2.reg[reg1]
    reg2 = (util2.fd['IR'] & 0x001F0000) >> 16
    util2.dx['B'] = util2.reg[reg2]
    util2.dx['RT'] = (util2.fd['IR'] & 0x001F0000) >> 16
    util2.dx['RD'] = (util2.fd['IR'] & 0x0000F800) >> 11
    imm = (util2.fd['IR'] & 0x0000FFFF) >> 0
    util2.dx['IMM'] = imm
    util2.dx['RS'] = (util2.fd['IR'] & 0x03E00000) >> 21
def EX():
    util.ran['EX'] = util.ran['ID']
    util.idle['EX'] = False
    util2.xmc['MEM_TO_REG'] = util2.dxc['MEM_TO_REG']
    util2.xmc['REG_WRITE'] = util2.dxc['REG_WRITE']
    util2.xmc['BRANCH'] = util2.dxc['BRANCH']
    util2.xmc['MEM_READ'] = util2.dxc['MEM_READ']
    util2.xmc['MEM_WRITE'] = util2.dxc['MEM_WRITE']
    util2.xm['BR_TGT'] = util2.dx['NPC'] + (util2.dx['IMM'] << 2)
    aluA = util.outFwdA
    if util2.dxc['ALU_SRC'] == 1: aluB = util2.dx['IMM']
    else: aluB = util.outFwdB
    if aluA - aluB == 0: util2.xm['ZERO'] = 1
    else: util2.xm['ZERO'] = 0
    out = 0
    if util2.dxc['ALU_OP'] == 0: out = aluA + aluB
    elif util2.dxc['ALU_OP'] == 1: out = aluA - aluB
    elif util2.dxc['ALU_OP'] == 2:
        funct = util2.dx['IMM'] & 0x0000003F
        shamt = util2.dx['IMM'] & 0x000007C0
        if funct == util.rwords['add']: out = aluA + aluB
        elif funct == util.rwords['sub']: out = aluA - aluB
        elif funct == util.rwords['and']: out = aluA & aluB
        elif funct == util.rwords['or']: out = aluA | aluB
        elif funct == util.rwords['sll']: out = aluA << shamt
        elif funct == util.rwords['srl']: out = aluA >> shamt
        elif funct == util.rwords['xor']: out = aluA ^ aluB
        elif funct == util.rwords['nor']: out = ~(aluA | aluB)
        elif funct == util.rwords['mult']: out = aluA * aluB
        elif funct == util.rwords['div']: out = aluA // aluB
    util2.xm['ALU_OUT'] = out
    util2.xm['B'] = util.outFwdB
    if util2.dxc['REG_DST'] == 1: util2.xm['RD'] = util2.dx['RD']
    else: util2.xm['RD'] = util2.dx['RT']
def MEM():
    util.ran['MEM'] = util.ran['EX']
    util.idle['MEM'] = util2.xmc['MEM_READ'] != 1 and util2.xmc['MEM_WRITE'] != 1
    util2.mwc['MEM_TO_REG'] = util2.xmc['MEM_TO_REG']
    util2.mwc['REG_WRITE'] = util2.xmc['REG_WRITE']
    if util2.xmc['MEM_READ'] == 1:
        if util2.xm['ALU_OUT']//4 < util.dsize: util2.mw['LMD'] = util2.data[util2.xm['ALU_OUT']//4]
        else:
            print('***WARNING***')
            print(f'\tMemory Read at position {util2.xm["ALU_OUT"]} not executed:')
            print(f'\t\tMemory only has {util.dsize*4} positions.')            
            try: input('Press ENTER to continue execution or abort with CTRL-C. ')
            except KeyboardInterrupt:
                print('Execution aborted.')
                exit()
    if util2.xmc['MEM_WRITE'] == 1:
        if util2.xm['ALU_OUT']//4 < util.dsize: util2.data[util2.xm['ALU_OUT']//4] = util2.xm['B']
        else:
            print('***WARNING***')
            print(f'\tMemory Write at position {util2.xm["ALU_OUT"]} not executed:')
            print(f'\t\tMemory only has {util.dsize*4} positions.')
            try: input('Press ENTER to continue execution or abort with CTRL-C. ')
            except KeyboardInterrupt:
                print('Execution aborted.')
                exit()
    util2.mw['ALU_OUT'] = util2.xm['ALU_OUT']
    util2.mw['RD'] = util2.xm['RD']
def WB():
    util.ran['WB'] = util.ran['MEM']
    util.idle['WB'] = util2.mwc['REG_WRITE'] != 1 or util2.mw['RD'] == 0
    if util2.mwc['REG_WRITE'] == 1 and util2.mw['RD'] != 0:
        if util2.mwc['MEM_TO_REG'] == 1: util2.reg[util2.mw['RD']] = util2.mw['LMD']
        else: util2.reg[util2.mw['RD']] = util2.mw['ALU_OUT']