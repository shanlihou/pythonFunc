import os
import sys
import config


dataPath = os.path.join(config.root, r'Dev\Server\kbeWin\kbengine\assets\scripts\server_common')
sys.path.append(dataPath)
dataPath = os.path.join(config.root, r'Dev\Server\kbeWin\kbengine\assets\scripts\data')
sys.path.append(dataPath)
dataPath = os.path.join(config.root, r'Dev\Server\kbeWin\kbengine\assets\scripts\user_type')
sys.path.append(dataPath)
import gameconst
import building_spaceGate as BSGD
import plunder_set as PSD
import systemWorld as SWD
import monsterStandardProp_prop as MPPD
import rewardData_rewardData as RDDT
# import itemData_itemData as IDIDD
import building_cangku as BCKD
import building_base
import building_explore as BED
import formula_generalFormula as FGFD

if __name__ == '__main__':
    pass