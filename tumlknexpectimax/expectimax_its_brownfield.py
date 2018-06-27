"""
Expectimax search for a mix of business, residential and Brownfield ITS subscribers.
Assumptions are: a. 7% business subscribers in urban area, b. Businesses charged more for 1:1 contention ratio
c. 10% IRR d. 10% Customer churn for both business as well as residential users. Monopolistic scenario, no competition
*************************************************************************************************
1. Enter the details like capex,opex,revenue and generate data for each of the technologies
2. update migration dictionary according to technology number
3. Upgrade techindex according to technology name
4. Provide the years (keep gap under 15 years) and run the algorithm.
************************************************************************************************
File: expectimax_business.py
Functionality: Runs expectimax
Author: Sai Kireet Patri
Copyright: Technische Universitaet Muenchen
"""

from tumlknexpectimax.input_parser import xls_parser
from tumlknexpectimax.model_present_value.present_value import GeneratePresentValue
from tumlknexpectimax.tree.build_tree import TreeBuilder
from tumlknexpectimax.output_parser.create_output_json import OutputJSON
from tumlknexpectimax.output_parser.create_output_graphs import OutputGraphs
import copy
import time
import sys
import os
# TODO: 10-05-2018: Update for hybridpon


class ExpectiNPVITSBrownfield:
    """

    """
    # Class variable
    action_dict = {}

    def __init__(self, filename,START_YEAR, MAX_YEAR, pen_curve, depth_100, only_ftth=False):
        self.xparse = xls_parser.Parser()

        capex_values, opex_values, mig_matrix = self.xparse.xls_parse_business(filename) # 'input_data_residential.xlsx'

        self.capex_values_dict = capex_values.to_dict()
        self.opex_values = opex_values['Approx OPEX per year'].to_dict()
        self.mig_matrix = mig_matrix.to_dict()

        self.techindex = {0:u'ADSL',1:u'FTTC_GPON_25',2:u'FTTB_XGPON_50', 3:u'FTTB_UDWDM_50',
                           4:u'FTTH_UDWDM_100', 5:u'FTTH_XGPON_100', 6:u'FTTC_GPON_100',
                          7:u'FTTB_XGPON_100', 8:u'FTTB_UDWDM_100', 9:u'FTTC_Hybridpon_25',
                          10:u'FTTB_Hybridpon_50', 11:u'FTTH_Hybridpon_100', 12:u'FTTC_Hybridpon_100',
                          13:u'FTTB_Hybridpon_100'}
        self.data_rate = {0: 20, 1: 25, 2: 50, 3: 50, 4: 100, 5: 100, 6: 100, 7: 100, 8: 100, 9: 25, 10: 50, 11: 100, 12: 100, 13: 100}

        self.START_YEAR = START_YEAR
        self.MAX_YEAR = MAX_YEAR

        if not only_ftth:
            self.node_mig_dict_unforced = {0: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
                                           1: [1, 2, 5, 6, 7], 2: [2, 5, 7], 3: [3, 4, 8], 4: [4],5: [5],
                                           6: [5, 6, 7], 7: [7, 5], 8: [8, 4], 9: [9, 10, 11, 12, 13],
                                           10: [10, 11, 13], 11: [11], 12: [11, 12, 13], 13: [11, 13]}

            self.node_mig_dict_forced = {0: [4, 5, 6, 7, 8, 11, 12, 13], 1: [5, 6], 2: [5, 7], 3: [4, 8], 4: [4],
                                         5: [5], 6: [5, 6, 7], 7: [7, 5], 8: [8, 4], 9: [11, 12, 13], 10: [11, 13],
                                         11: [11], 12: [11, 12, 13], 13: [11, 13]}

        else:
            self.node_mig_dict_unforced = {0: [0, 1, 2, 3, 4, 5, 9, 10, 11], 1: [1, 2, 5], 2: [2, 5],
                                           3: [3, 4], 4: [4],5: [5], 6: [5, 6, 7], 7: [7, 5], 8: [8, 4],
                                       9: [9, 10, 11], 10: [10, 11], 11: [11], 12: [11, 12, 13],
                                       13: [11, 13]}
            self.node_mig_dict_forced = {0: [4, 5, 11], 1: [5], 2: [5], 3: [4], 4: [4], 5: [5],
                                     6: [5, 6, 7], 7: [7, 5], 8: [8, 4], 9: [11], 10: [11], 11: [11],
                                     12: [11,12,13], 13: [11,13]}
        self.action_list = []
        self.pen_curve = pen_curve
        self.path_list = []
        self.force_depth = depth_100
        self.disc_rate = 0.1
        self.present_value_gen = GeneratePresentValue('its',self.pen_curve,self.disc_rate,self.capex_values_dict,self.opex_values)

    def build_its_tree(self, start_node_tech, mean_prob):

        treeBuild = TreeBuilder(self.node_mig_dict_forced,self.node_mig_dict_unforced,self.capex_values_dict,
                                self.techindex,self.mig_matrix,self.pen_curve,self.path_list,
                                self.force_depth,self.START_YEAR,self.MAX_YEAR,self.present_value_gen)

        time_interval_cf,next_tech,intermediate_path_dict = treeBuild.build_mini_tree(self.action_list,
                                                                                      self.node_mig_dict_unforced,
                                                                                      start_node_tech,mean_prob,
                                                                                      self.pen_curve)
        return time_interval_cf,next_tech,intermediate_path_dict


def run_expecti_its(inputfile, startyear, maxyear, penetration_curve,depth_all_100,only_ftth):

        start = startyear
        end = maxyear
        start_node_tech = 0

        tech_changes_at_intervals = []
        t1 = time.time()
        filename = inputfile
        # TODO: BUILD TREE COMES HERE
        expectiTreeLikely = ExpectiNPVITSBrownfield(filename,start, end,penetration_curve,depth_all_100,only_ftth)
        time_interval_cf,next_tech,intermediate_path_list = expectiTreeLikely.build_its_tree(start_node_tech,0.1)
        tech_changes_at_intervals.append(next_tech)
        action_list = expectiTreeLikely.action_list
        t2 = time.time()
        final_migration_year = startyear
        action_list_new = [expectiTreeLikely.techindex[tech] for tech in action_list]
        if len(action_list) !=(2038-startyear+1):
            action_list_new = [expectiTreeLikely.techindex[tech] for tech in action_list]
            last_tech = expectiTreeLikely.techindex[action_list[-1]]
            for year in range(startyear + len(action_list), maxyear):
                action_list_new.append(last_tech)

        time_taken = t2-t1
        expected_npv = time_interval_cf

        max_tech = 0
        for tech_num in intermediate_path_list:
            if tech_num >= max_tech:
                max_tech = tech_num
        # Now we have max tech
        current_tech = 0
        mig_years_dict = {}
        for year_index in range(0,len(intermediate_path_list)):
            if intermediate_path_list[year_index] != current_tech:
                mig_years_dict[startyear+year_index] = expectiTreeLikely.techindex[intermediate_path_list[year_index]]

            if intermediate_path_list[year_index] == max_tech:
                # mig_years.append(startyear+year_index)
                final_migration_year = startyear+year_index

            current_tech = intermediate_path_list[year_index]
        max_data_rate = expectiTreeLikely.data_rate[max_tech]
        # "NPV_expected","mig_path","year_to_final_tech","mig_years","final_data_rate", "total_time"

        if not action_list_new:
            return expected_npv, action_list, final_migration_year, mig_years_dict, max_data_rate, time_taken
        else:
            return expected_npv, action_list_new, final_migration_year, mig_years_dict, max_data_rate, time_taken


if __name__ == "__main__":

    if len(sys.argv) < 2:

        print('This script needs the following parameters')
        print("input_file name stored in the current working directory of script eg: input_data.xlsx")
        print('start year eg 2018')
        print('end year eg 2038')
        print('Look ahead horizon for the agent, eg: 5,10,15. Do not cross 15')
    print('Optical Network Migration Planning Tool\n')
    print('Copyright: Chair of Communication Networks, Technical University of Munich, 2018\n')
    print ('For different penetration curves, returns the expected NPV and path taken to reach final technology')
    print('Business Case: Residential+Business+ITS Customers')
    input_file = sys.argv[1]
    start_year = sys.argv[2]
    end_year = sys.argv[3]
    result_filename = 'results_expectimax_its'
    output_parser = OutputJSON(result_filename)
    # final_migration_dict = {}
    print('----------------------------------------------------------------------------------------------------')
    for ftth_flag in [True,False]:
        print('----------------------------------------------------------------------------------------------------')
        for depth in [25,7]:
            print('-----------------------------------------------------------------------------------------------')
            print('Year at which all users to be moved to FTTH: {0}'.format(depth))
            mig_info_pen_dict = {}
            for pen_curve in ['Cons PV','Likely PV', 'Aggr PV']:

                expected_npv, action_list_new, final_migration_year, mig_years, max_data_rate, time_taken=\
                    run_expecti_its(input_file,int(start_year),int(end_year),pen_curve,depth,ftth_flag)
                mig_info_pen_dict[pen_curve] = output_parser.build_mig_dict(pen_curve,expected_npv,action_list_new,final_migration_year,mig_years,max_data_rate,time_taken)

            output_parser.is_ftth_dict[(ftth_flag,depth)] = copy.deepcopy(mig_info_pen_dict)
            mig_info_pen_dict = {}


    # TODO: JSONIFY THE OUTPUT and generate graphs

    # Dump to json file
    output_parser.dump_to_json(output_parser.is_ftth_dict)
    # grapher = OutputGraphs(os.path.join(os.getcwd(),'..'))
    # grapher.create_npv_graph(0)
    # grapher.create_migration_steps(0)



