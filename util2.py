import util
pc = 0
inst = []
reg = [0 for i in range(32)]
data = [0 for i in range(util.dsize)]
fd = {'NPC': 0, 'IR': 0}
dx = {'NPC': 0, 'A': 0, 'B': 0, 'RT': 0, 'RD': 0, 'IMM': 0, 'RS': 0}
xm = {'BR_TGT': 0, 'ZERO': 0, 'ALU_OUT': 0, 'B': 0, 'RD': 0}
mw = {'LMD': 0, 'ALU_OUT': 0, 'RD': 0}
dxc = {'REG_DST': 0, 'ALU_SRC': 0, 'MEM_TO_REG': 0, 'REG_WRITE': 0, 'MEM_READ': 0, 'MEM_WRITE': 0, 'BRANCH': 0, 'ALU_OP': 0}
xmc = {'MEM_READ': 0, 'MEM_WRITE': 0, 'BRANCH': 0, 'MEM_TO_REG': 0, 'REG_WRITE': 0}
mwc = {'MEM_TO_REG': 0, 'REG_WRITE': 0}
fwd = {'PC_WRITE': 1, 'IF_ID_WRITE': 1, 'FWD_A': 0, 'FWD_B': 0, 'STALL': 0}
