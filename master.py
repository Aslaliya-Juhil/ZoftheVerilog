import sys
import translate
import stage
import util3
import util2, util
def main():
    try: filename = next(arg for arg in sys.argv[1:] if not arg.startswith('-'))
    except StopIteration: filename = "/home/juhil/Workspace/python/ES215_project/program.asm"
    program = util3.readFile(filename)
    programLength = len(program)
    for i in range(programLength):
        if not program[i] or program[i][0] == '#': continue
        encoded = translate.encode(program[i].split('#')[0])
        if encoded not in util.e: util2.inst.append(encoded)
        else:
            print(f'e @ \'{filename}\':')
            print(f'\tLine {i+1}: \'{program[i]}\'')
            if encoded == util.ei: print('\t\tCouldn\'t parse the instruction')
            elif encoded == util.ea: print('\t\tCouldn\'t parse one or more arguments')
            elif encoded == util.ef: print('\t\tOne or more arguments are under/overflowing')
            return
    util3.printInstMem()
    print()
    silent = ('-s' in sys.argv)
    skipSteps = silent
    clkHistory = []
    clk = 0
    while clk == 0 or (util.ran['IF'][1] != 0 or util.ran['ID'][1] != 0 or util.ran['EX'][1] != 0 or util.ran['MEM'][1] != 0):
        if silent: print(' '.join(['─'*20, f'CLK #{clk}', '─'*20]))
        else: print(' '.join(['─'*38, f'CLK #{clk}', '─'*38]))
        clkHistory.append([])
        stage.EX_fwd()
        stage.WB()
        stage.MEM()
        stage.EX()
        stage.ID()
        stage.IF()
        stage.ID_hzd()
        for i in range(len(util2.reg)): util2.reg[i] &= 0xFFFFFFFF
        for i in range(len(util2.data)): util2.data[i] &= 0xFFFFFFFF
        for stg in ['IF', 'ID', 'EX', 'MEM', 'WB']:
            if util.ran[stg][1] != 0:
                idle = ' (idle)' if util.idle[stg] else ''
                clkHistory[clk].append((stg, util.ran[stg], util.idle[stg]))
                print(f'> Stage {stg}: #{util.ran[stg][0]*4} = [{translate.decode(util.ran[stg][1])}]{idle}.')
        if not silent:
            print('─'*(83+len(str(clk))))
            util3.printPC()
            if util.data_hzd or util.ctrl_hzd: util3.printFwdAndHazard()
            util3.printPipelineRegs()
            util3.printRegMem()
            util3.printDataMem()
            print('─'*(83+len(str(clk))))
        clk += 1
        if not skipSteps:
            try:
                opt = input('| step: [ENTER] | end: [E|Q] | ').lower()
                skipSteps = (opt == 'e' or opt == 'q')
            except KeyboardInterrupt:
                print('\nExecution aborted.')
                exit()
    if silent:
        print()
        util3.printPipelineRegs()
        util3.printRegMem()
        util3.printDataMem()
    else: print('Empty pipeline, ending execution...')
    print()
    print(f'Program ran in {clk} clocks.')
    print()
    util3.printHistory(clkHistory)
    return
if __name__ == '__main__':
    if sys.platform == 'win32': 
        sys.stdout.reconfigure(encoding='UTF-8')
main()