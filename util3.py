import translate
import util2, util
def readFile(filename):
    content = []
    with open(filename, 'r', encoding='UTF-8') as f:
        for l in f:
            s = l.strip()
            if s: content.append(s)
    return content
def printFwdAndHazard():
    print('               ╔═════════════[FORWARDING AND HAZARD UNITS]══════════════╗')
    if util2.fwd['PC_WRITE'] == 1 and util2.fwd['IF_ID_WRITE'] == 1 and util2.fwd['FWD_A'] == 0 and util2.fwd['FWD_B'] == 0: print('               ║ No action.                                             ║')
    else:
        if (util2.fwd['PC_WRITE'] == 0 and util2.fwd['IF_ID_WRITE'] == 0) or (util2.dxc['BRANCH'] == 1 or util2.xmc['BRANCH'] == 1): print('               ║ Stalling (blocking write on PC and IF/ID)...           ║')
        if util2.fwd['FWD_A'] != 0: print('               ║ FWD_A={} (MEM/WB.ALU_OUT -> A)...                       ║'.format(util2.fwd['FWD_A']))
        if util2.fwd['FWD_B'] != 0: print('               ║ FWD_B={} (MEM/WB.ALU_OUT -> Mux @ aluB and EX/MEM.B)... ║'.format(util2.fwd['FWD_B']))
    print('               ╚════════════════════════════════════════════════════════╝')
def printPipelineRegs():
    print('╔════════════════════╦═══════════[PIPELINE REGISTERS]══════════╦════════════════════╗')
    print('║      [IF/ID]       ║      [ID/EX]       ║      [EX/MEM]      ║      [MEM/WB]      ║')
    print('║════════════════════╬════════════════════╬════════════════════╬════════════════════║')
    print('║                    ║     MEM_TO_REG=[{}] ║     MEM_TO_REG=[{}] ║     MEM_TO_REG=[{}] ║'.format(util2.dxc['MEM_TO_REG'], util2.xmc['MEM_TO_REG'], util2.mwc['MEM_TO_REG']))
    print('║                    ║      REG_WRITE=[{}] ║      REG_WRITE=[{}] ║      REG_WRITE=[{}] ║'.format(util2.dxc['REG_WRITE'], util2.xmc['REG_WRITE'], util2.mwc['REG_WRITE']))
    print('║                    ║         BRANCH=[{}] ║         BRANCH=[{}] ║                    ║'.format(util2.dxc['BRANCH'], util2.xmc['BRANCH']))
    print('║                    ║       MEM_READ=[{}] ║       MEM_READ=[{}] ║                    ║'.format(util2.dxc['MEM_READ'], util2.xmc['MEM_READ']))
    print('║                    ║      MEM_WRITE=[{}] ║      MEM_WRITE=[{}] ║                    ║'.format(util2.dxc['MEM_WRITE'], util2.xmc['MEM_WRITE']))
    print('║                    ║        REG_DST=[{}] ║                    ║                    ║'.format(util2.dxc['REG_DST']))
    print('║                    ║        ALU_SRC=[{}] ║                    ║                    ║'.format(util2.dxc['ALU_SRC']))
    print('║                    ║        ALU_OP=[{:02b}] ║                    ║                    ║'.format(util2.dxc['ALU_OP']))
    print('╠════════════════════╬════════════════════╬════════════════════╬════════════════════╣')
    print('║     NPC=[{:08X}] ║     NPC=[{:08X}] ║  BR_TGT=[{:08X}] ║                    ║'.format(util2.fd['NPC'], util2.dx['NPC'], util2.xm['BR_TGT']))
    print('║                    ║       A=[{:08X}] ║    ZERO=[{:08X}] ║     LMD=[{:08X}] ║'.format(util2.dx['A'], util2.xm['ZERO'], util2.mw['LMD']))
    print('║      IR=[{:08X}] ║       B=[{:08X}] ║ ALU_OUT=[{:08X}] ║                    ║'.format(util2.fd['IR'], util2.dx['B'], util2.xm['ALU_OUT']))
    print('║                    ║      RT=[{:08X}] ║       B=[{:08X}] ║ ALU_OUT=[{:08X}] ║'.format(util2.dx['RT'], util2.xm['B'], util2.mw['ALU_OUT']))
    print('║                    ║      RD=[{:08X}] ║      RD=[{:08X}] ║      RD=[{:08X}] ║'.format(util2.dx['RD'], util2.xm['RD'], util2.mw['RD']))
    print('║                    ║     IMM=[{:08X}] ║                    ║                    ║'.format(util2.dx['IMM']))
    if util.data_hzd or util.ctrl_hzd: print('║                    ║      RS=[{:08X}] ║                    ║                    ║'.format(util2.dx['RS']))
    print('╚════════════════════╩════════════════════╩════════════════════╩════════════════════╝')
def printPC():
    print('                                   ╔════[PC]════╗')
    print('                                   ║ [{:08X}] ║'.format(util2.pc))
    print('                                   ╚════════════╝')
def printInstMem():
    print('╔═════╦═════════════════════════════[PROGRAM]═══════════╦════════════════════════╗')
    for i in range(len(util2.inst)): print('║ {:>3} ║ 0x{:08X} = 0b{:032b} ║ {:<22} ║'.format(i*4, util2.inst[i], util2.inst[i], translate.decode(util2.inst[i])))
    print('╚═════╩═════════════════════════════════════════════════╩════════════════════════╝')
def printRegMem():
    print('╔════════════════════╦═══════════════[REGISTERS]═══════════════╦════════════════════╗')
    print('║ $00[ 0]=[{:08X}] ║ $t0[ 8]=[{:08X}] ║ $s0[16]=[{:08X}] ║ $t8[24]=[{:08X}] ║'.format(util2.reg[0], util2.reg[8], util2.reg[16], util2.reg[24]))
    print('║ $at[ 1]=[{:08X}] ║ $t1[ 9]=[{:08X}] ║ $s1[17]=[{:08X}] ║ $t9[25]=[{:08X}] ║'.format(util2.reg[1], util2.reg[9], util2.reg[17], util2.reg[25]))
    print('║ $v0[ 2]=[{:08X}] ║ $t2[10]=[{:08X}] ║ $s2[18]=[{:08X}] ║ $k0[26]=[{:08X}] ║'.format(util2.reg[2], util2.reg[10], util2.reg[18], util2.reg[26]))
    print('║ $v1[ 3]=[{:08X}] ║ $t3[11]=[{:08X}] ║ $s3[19]=[{:08X}] ║ $k1[27]=[{:08X}] ║'.format(util2.reg[3], util2.reg[11], util2.reg[19], util2.reg[27]))
    print('║ $a0[ 4]=[{:08X}] ║ $t4[12]=[{:08X}] ║ $s4[20]=[{:08X}] ║ $gp[28]=[{:08X}] ║'.format(util2.reg[4], util2.reg[12], util2.reg[20], util2.reg[28]))
    print('║ $a1[ 5]=[{:08X}] ║ $t5[13]=[{:08X}] ║ $s5[21]=[{:08X}] ║ $sp[29]=[{:08X}] ║'.format(util2.reg[5], util2.reg[13], util2.reg[21], util2.reg[29]))
    print('║ $a2[ 6]=[{:08X}] ║ $t6[14]=[{:08X}] ║ $s6[22]=[{:08X}] ║ $fp[30]=[{:08X}] ║'.format(util2.reg[6], util2.reg[14], util2.reg[22], util2.reg[30]))
    print('║ $a3[ 7]=[{:08X}] ║ $t7[15]=[{:08X}] ║ $s7[23]=[{:08X}] ║ $ra[31]=[{:08X}] ║'.format(util2.reg[7], util2.reg[15], util2.reg[23], util2.reg[31]))
    print('╚════════════════════╩════════════════════╩════════════════════╩════════════════════╝')
def printDataMem():
    print('    ╔══════════════════╦═══════════════[MEMORY]══════════════╦══════════════════╗')
    memSize = len(util2.data)
    for i in range(memSize//4):
        a, b, c, d = i*4, (memSize)+i*4, (memSize*2)+i*4, (memSize*3)+i*4
        print('    ║ [{:03}]=[{:08X}] ║ [{:03}]=[{:08X}] ║ [{:03}]=[{:08X}] ║ [{:03}]=[{:08X}] ║'.format(a, util2.data[a//4], b, util2.data[b//4], c, util2.data[c//4], d, util2.data[d//4]))        
    print('    ╚══════════════════╩══════════════════╩══════════════════╩══════════════════╝')
def printHistory(clkHistory):
    history = [[' ' for i in range(len(clkHistory))] for i in range(len(util2.inst))]
    for i in range(len(clkHistory)):
        for exe in clkHistory[i]:
            if exe[2]: history[exe[1][0]][i] = ' '
            else: history[exe[1][0]][i] = exe[0]
    print('╔═════╦════════════════════════╦' + '═'*(6*len(clkHistory)) + '╗')
    print('║ Mem ║ ' + 'Clock #'.center(22) + ' ║', end='')
    for i in range(len(clkHistory)): print(str(i).center(5), end=' ')
    print('║')
    print('╠═════╬════════════════════════╬' + '═'*(6*len(clkHistory)) + '╣')
    for i in range(len(history)):
        print('║ {:>3} ║ {:>22} ║'.format(i*4, translate.decode(util2.inst[i])), end='')
        for j in range(len(history[0])): print(history[i][j].center(5), end=' ')
        print('║')
    print('╚═════╩════════════════════════╩' + '═'*(6*len(clkHistory)) + '╝')