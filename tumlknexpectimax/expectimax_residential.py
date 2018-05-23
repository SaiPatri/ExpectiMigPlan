"""
Expectimax search for residenial subscribers.
1. Enter the details like capex,opex,revenue and generate data for each of the technologies
2. update migration dictionary according to technology number
3. Upgrade techindex according to technology name
4. Provide the years and run the algorithm.

File: expectimax_residential.py
Functionality: Runs expectimax
Author: Sai Kireet Patri
Copyright: Technische Universitaet Muenchen
"""

from tumlknexpectimax.input_parser import xls_parser
from tumlknexpectimax.tree.build_tree import TreeBuilder

import time
import sys

# TODO: 10-05-2018: Update for hybridpon


class ExpectiNPV:
    """

    """
    # Class variable
    action_dict = {}

    def __init__(self, filename,START_YEAR, MAX_YEAR, pen_curve):
        self.xparse = xls_parser.Parser()
        parsed_adsl_0,parsed_fttc_1,parsed_fttb_2, \
        parsed_fttb_3, parsed_ftth_4, parsed_ftth_5, parsed_fttc_6_force, parsed_fttb_7_force, parsed_fttb_8_force, \
        parsed_fttc_hybridpon_9, parsed_fttb_hybridpon_10, parsed_ftth_hybridpon_11, parsed_fttc_hybridpon_12_force, \
        parsed_fttb_hybridpon_13_force, capex_values, mig_matrix = self.xparse.xls_parse_residential(filename) # 'input_data_residential.xlsx'

        self.pv_dict = {0: parsed_adsl_0.to_dict(),1: parsed_fttc_1.to_dict(), 2:parsed_fttb_2.to_dict(),
                        3:parsed_fttb_3.to_dict(), 4: parsed_ftth_4.to_dict(), 5:parsed_ftth_5.to_dict(),
                        6: parsed_fttc_6_force.to_dict(), 7:parsed_fttb_7_force.to_dict(),
                        8: parsed_fttb_8_force.to_dict(), 9: parsed_fttc_hybridpon_9.to_dict(),
                        10: parsed_fttb_hybridpon_10.to_dict(), 11: parsed_ftth_hybridpon_11.to_dict(),
                        12: parsed_fttc_hybridpon_12_force.to_dict(), 13: parsed_fttb_hybridpon_13_force.to_dict()}

        self.capex_values_dict = capex_values.to_dict()

        self.mig_matrix = mig_matrix.to_dict()

        self.techindex = {0:u'ADSL',1:u'FTTC_2_STAGE_GPON',2:u'FTTB_2_STAGE_XGPON', 3:u'FTTB_1_STAGE_UDWDM_GF',
                           4:u'FTTH_2_STAGE_UDWDM', 5:u'FTTH_2_STAGE_XGPON', 6:u'FTTC_2_STAGE_GPON_FORCE',
                          7:u'FTTB_2_STAGE_XGPON_FORCE', 8:u'FTTB_1_STAGE_UDWDM_FORCE', 9:u'FTTC_Hybridpon',
                          10:u'FTTB_Hybridpon', 11:u'FTTH_Hybridpon', 12:u'FTTC_Hybridpon_FORCE',
                          13:u'FTTB_Hybridpon_FORCE'}

        self.START_YEAR = START_YEAR
        self.MAX_YEAR = MAX_YEAR
        # self.node_mig_dict = {0: [0,1,2,3,4,5,6,7,8], 1: [1, 2, 5, 6, 7], 2: [2, 5, 7], 3: [3, 4, 8], 4: [4],5: [5], 6: [5, 6, 7], 7: [4, 5, 7], 8: [8]}
        """
        self.node_mig_dict_unforced = {0: [0,1,2,3,4,5,6,7,8,9,10,11,12,13], 1: [1, 2, 5, 6, 7], 2: [2, 5, 7],
                                       3: [3, 4, 8], 4: [4],5: [5], 6: [5, 6, 7], 7: [7, 5], 8: [8, 4],
                                       9: [9, 10, 11, 12, 13], 10: [10, 11, 13], 11: [11], 12: [11, 12, 13],
                                       13: [11, 13]}
                                       
        self.node_mig_dict_forced = {0: [4, 5, 6, 7, 8, 11, 12, 13], 1: [5, 6], 2: [5, 7], 3: [4, 8], 4: [4], 5: [5],
                                     6: [5, 6, 7], 7: [7, 5], 8: [8, 4], 9: [11, 12, 13], 10: [11, 13], 11: [11],
                                     12: [11,12,13], 13: [11,13]}
                        
        """
        self.node_mig_dict_unforced = {0: [0,1,2,3,4,5,9,10,11], 1: [1, 2, 5], 2: [2, 5],
                                       3: [3, 4], 4: [4],5: [5], 6: [5, 6, 7], 7: [7, 5], 8: [8, 4],
                                       9: [9, 10, 11], 10: [10, 11], 11: [11], 12: [11, 12, 13],
                                       13: [11, 13]}
        self.node_mig_dict_forced = {0: [4, 5, 11], 1: [5], 2: [5], 3: [4], 4: [4], 5: [5],
                                     6: [5, 6, 7], 7: [7, 5], 8: [8, 4], 9: [11], 10: [11], 11: [11],
                                     12: [11,12,13], 13: [11,13]}


        self.action_list = []
        self.pen_curve = pen_curve
        self.path_list = []
        self.force_depth = 25
        # self.disc_rate = 0.1

    def build_residential_tree(self, start_node_tech, prob):

        treeBuild = TreeBuilder(self.node_mig_dict_forced,self.node_mig_dict_unforced,self.capex_values_dict,
                                     self.techindex,self.mig_matrix,self.pv_dict,self.pen_curve,self.path_list,
                                     self.force_depth,self.START_YEAR,self.MAX_YEAR)

        time_interval_cf,next_tech,intermediate_path_dict = treeBuild.build_mini_tree(self.action_list,
                                                                                           self.node_mig_dict_unforced,
                                                                                           start_node_tech,prob,
                                                                                           self.pen_curve)
        return time_interval_cf,next_tech,intermediate_path_dict


def run_expecti_residential(inputfile, startyear, maxyear, penetration_curve):

        # action_list = []
        start = startyear
        end = maxyear
        start_node_tech = 0
        intermediate_path_list = []
        tech_changes_at_intervals = []
        t1 = time.time()
        filename = inputfile
        # TODO: BUILD TREE COMES HERE
        expectiTreeLikely = ExpectiNPV(filename,start, end,penetration_curve)
        time_interval_cf,next_tech,intermediate_path_dict = expectiTreeLikely.build_residential_tree(start_node_tech,0.1)
        intermediate_path_list.append(intermediate_path_dict)
        tech_changes_at_intervals.append(next_tech)
        action_list = expectiTreeLikely.action_list
        t2 = time.time()
        action_list_new = []
        if len(action_list) is not maxyear - startyear:
            action_list_new = [expectiTreeLikely.techindex[tech] for tech in action_list]
            last_tech = expectiTreeLikely.techindex[action_list[-1]]
            for year in range(startyear + len(action_list), maxyear):
                action_list_new.append(last_tech)

        print ("Time took is: "+str((t2-t1)/60.0)+" minutes")
        print('Maximum reward generated is',time_interval_cf)
        print('The complete path is',intermediate_path_list)
        print ('Technology after year gaps', tech_changes_at_intervals)
        if not action_list_new:
            print ('Total tree is', action_list)
        else:
            print('Total tree is',action_list_new)


if __name__ == "__main__":

    if len(sys.argv) < 2:

        print ('This script needs the following parameters')
        print ("input_file name stored in the current working directory of script eg: input_data.xlsx")
        print ('start year eg 2018')
        print ('end year eg 2038')
        print('Look ahead horizon for the agent, eg: 5,10,15. Do not cross 15')
    print('Optical Network Migration Planning Tool\n')
    print('Copyright: Chair of Communication Networks, Technical University of Munich, 2018\n')
    print ('For different penetration curves, returns the expected NPV and path taken to reach final technology')
    input_file = sys.argv[1]
    start_year = sys.argv[2]
    end_year = sys.argv[3]

    for pen_curve in ['Cons PV','Likely PV', 'Aggr PV']:
        run_expecti_residential(input_file,int(start_year),int(end_year),pen_curve)

