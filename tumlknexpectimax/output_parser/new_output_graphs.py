"""
Creates the following graphs:
1. Net Present Values in all scenario all cases
2. Migration steps in all scenario all cases
"""
import json
import os
import sys
from collections import OrderedDict
from tumlknexpectimax.texplt  import texSaveFig,texFigure
import matplotlib.pyplot as plt
import numpy as np


class OutputGraphs:
    """

    """
    def __init__(self,json_directory):
        self.json_dir = json_directory
        self.residential_json_file = "results_expectimax_residential.json"
        self.business_json_file = "results_expectimax_business.json"
        self.its_json_file = "results_expectimax_its.json"
        pass

    def create_npv_graph(self,scenario=0):
        """
        scenario 0 for residential, scenario 1 for business, scenario 2 for ITS
        Create NPV graphs using matplotlib
        :return:
        """
        # Read residential json file
        if scenario == 0:

            results_json_file = os.path.join(self.json_dir,self.residential_json_file)
            scenario_name = 'Residential'
        elif scenario == 1:
            results_json_file = os.path.join(self.json_dir,self.business_json_file)
            scenario_name = 'Residential+Business'
        else:
            results_json_file = os.path.join(self.json_dir,self.its_json_file)
            scenario_name = 'Residential+Business+ITS'
        with open(results_json_file) as jsonfile:
            migration_data = json.load(jsonfile)
        expected_npv_cons = []
        expected_npv_likely = []
        expected_npv_aggr = []
        # Set up the graph
        # no. of scenarios is 4, each scenario has 3 bars
        index_bar = np.arange(4)
        width = 0.25
        texFigure(10,8,1,9,100)
        fig,ax = plt.subplots()
        index = 0
        for ftth_flag in ['false','true']:
            for forced_depth in ['25','7']:
                for pen_curve in ['Cons PV', 'Likely PV', 'Aggr PV']:
                    if pen_curve == 'Cons PV':
                        expected_npv_cons.append(migration_data[index]['migration_info'][pen_curve]['NPV_expected'])
                    elif pen_curve == 'Likely PV':
                        expected_npv_likely.append(migration_data[index]['migration_info'][pen_curve]['NPV_expected'])
                    else:
                        expected_npv_aggr.append(migration_data[index]['migration_info'][pen_curve]['NPV_expected'])
                index += 1

        rects_cons = ax.bar(index_bar,expected_npv_cons,width,color='xkcd:purple')
        rects_likely = ax.bar(index_bar+width,expected_npv_likely,width,color='xkcd:orange')
        rects_aggr = ax.bar(index_bar+2*width,expected_npv_aggr,width,color='xkcd:dark teal')

        ax.set_ylabel('Net Present Value in Cost Units')
        ax.set_title('Expected NPV in {0} scenario for different penetration curves'.format(scenario_name))
        ax.set_xticks(index_bar + width/3)
        ax.set_yticks(np.arange(np.floor(min(expected_npv_cons)/1000.0)*1000.0-100000.0,np.ceil(max(expected_npv_aggr)/1000.0)*1000.0+200000.0,100000.0))
        ax.set_xticklabels(('Unforced to 100 Mbps\nFTTC/FTTB/FTTH', 'Unforced to 100 Mbps\nOnly FTTH', 'Forced to 100 Mbps\nFTTC/FTTB/FTTH','Forced to 100 Mbps\nOnly FTTH'))
        ax.legend((rects_cons[0], rects_likely[0], rects_aggr[0]), ('Conservative', 'Likely','Aggressive'))

        for rects in [rects_cons,rects_likely,rects_aggr]:
            if rects == rects_cons:
                npvlist = [float("{0:.2f}".format(npv)) for npv in expected_npv_cons]
            elif rects == rects_likely:
                npvlist = [float("{0:.2f}".format(npv)) for npv in expected_npv_likely]
            else:
                npvlist = [float("{0:.2f}".format(npv)) for npv in expected_npv_aggr]

            for rect, label in zip(rects, npvlist):
                height = rect.get_height()
                if label < 0:
                    ax.text(rect.get_x() + rect.get_width() / 2, -height - 15000, label,
                            ha='center', va='bottom')
                else:
                    ax.text(rect.get_x() + rect.get_width() / 2, height + 500, label,
                            ha='center', va='bottom')
        # plt.grid(True,which='major',axis='y')
        plt.axhline(0,color='k')
        texSaveFig("expected_npv.pdf")
        # plt.show(block=False)

    def churn_npv(self):
        expected_npv_5 = [152401.51, 273265.39, 1289079.80]
        expected_npv_10 = [152137.36, 272726.55, 1282631.54]
        expected_npv_20 = [145045.34, 263694.36, 1259358.38]
        # no of scenario is 3 each graph has 3 bars
        index_bar = np.arange(3)
        width = 0.25
        texFigure(10,8,1,14,100)
        fig,ax = plt.subplots()
        index = 0
        rects_5 = ax.bar(index_bar,expected_npv_5,width,color='xkcd:purple')
        rects_10 = ax.bar(index_bar+width,expected_npv_10,width,color='xkcd:orange')
        rects_20 = ax.bar(index_bar+2*width,expected_npv_20,width,color='xkcd:dark teal')
        ax.set_ylabel('Net Present Value in Cost Units')
        ax.set_title('Expected NPV for different churn rates')
        ax.set_xticks(index_bar + width/3)
        ax.set_yticks(np.arange(np.floor(min(expected_npv_5)/1000.0)*1000.0-100000.0,np.ceil(max(expected_npv_20)/1000.0)*1000.0+200000.0,100000.0))
        ax.set_xticklabels(('Conservative', 'Likely', 'Aggressive'))
        ax.legend((rects_5, rects_10, rects_20), ('Churn rate 0.05', 'Churn rate 0.1', 'Churn 0.2'))
        plt.axhline(0,color='k')
        texSaveFig("expected_npv_churn_sense_analysis.pdf")

    def comp_cost_npv(self):
        with open(os.path.join(self.json_dir,r"results_comp_cost.json")) as jsonfile:
            migration_data = json.load(jsonfile)
        expected_npv_cons = []
        expected_npv_likely = []
        expected_npv_aggr = []
        # Set up the graph
        # no. of scenarios is 4, each scenario has 3 bars
        # for opex, 2 scenarios
        index_bar = np.arange(4)# np.arange(4)
        width = 0.25
        texFigure(10,8,1,12,100)
        fig,ax = plt.subplots()
        index = 0
        for name in ['OASE','Phillipson','Rokkas','BSG']:# # # ['OASE Base Model','OASE new OPEX']: ['OASE','Phillipson','Rokkas','BSG']:
                print(migration_data[index]['name'])
                for pen_curve in ['Cons PV', 'Likely PV', 'Aggr PV']:
                    if pen_curve == 'Cons PV':
                        expected_npv_cons.append(migration_data[index]['migration_info'][pen_curve]['NPV_expected'])
                    elif pen_curve == 'Likely PV':
                        expected_npv_likely.append(migration_data[index]['migration_info'][pen_curve]['NPV_expected'])
                    else:
                        expected_npv_aggr.append(migration_data[index]['migration_info'][pen_curve]['NPV_expected'])
                index += 1

        rects_cons = ax.bar(index_bar,expected_npv_cons,width,color='xkcd:purple')
        rects_likely = ax.bar(index_bar+width,expected_npv_likely,width,color='xkcd:orange')
        rects_aggr = ax.bar(index_bar+2*width,expected_npv_aggr,width,color='xkcd:dark teal')

        ax.set_ylabel('Net Present Value in Cost Units')
        ax.set_title('Expected NPV for different Component Cost Studies')
        ax.set_xticks(index_bar + width/3)
        ax.set_yticks(np.arange(np.floor(min(expected_npv_cons)/1000.0)*1000.0-100000.0,np.ceil(max(expected_npv_aggr)/1000.0)*1000.0+200000.0,100000.0))
        ax.set_xticklabels(('OASE','Phillipson','Rokkas','BSG'))
        ax.legend((rects_cons[0], rects_likely[0], rects_aggr[0]), ('Conservative', 'Likely','Aggressive'))
        """"""
        for rects in [rects_cons,rects_likely,rects_aggr]:
            if rects == rects_cons:
                npvlist = [float("{0:.2f}".format(npv)) for npv in expected_npv_cons]
            elif rects == rects_likely:
                npvlist = [float("{0:.2f}".format(npv)) for npv in expected_npv_likely]
            else:
                npvlist = [float("{0:.2f}".format(npv)) for npv in expected_npv_aggr]

            for rect, label in zip(rects, npvlist):
                height = rect.get_height()
                if label < 0:
                    ax.text(rect.get_x() + rect.get_width() / 2, -height - 30000, label,
                            ha='center', va='bottom')
                else:
                    ax.text(rect.get_x() + rect.get_width() / 2, height + 500, label,
                            ha='center', va='bottom')
        # plt.grid(True,which='major',axis='y')
        plt.axhline(0,color='k')
        # plt.show()
        texSaveFig(r"expected_npv.pdf")# texSaveFig("expected_npv_comp_cost.pdf")
        # plt.show(block=False)


    def len_check(self, mig_tree,START_YEAR,END_YEAR):

        if len(mig_tree) > END_YEAR-START_YEAR:
            number_to_pop = len(mig_tree) - (END_YEAR-START_YEAR)
            mig_tree = mig_tree[:len(mig_tree)-number_to_pop]
        if len(mig_tree) < END_YEAR-START_YEAR:
            number_to_add = END_YEAR-START_YEAR-len(mig_tree)
            last_tech = mig_tree[-1]
            for num in range(0,number_to_add):
                mig_tree.append(last_tech)
        return mig_tree

    def make_fig_steps(self,index,mig_cons,mig_likely,mig_aggr):
        """

        :param mig_cons:
        :param mig_likely:
        :param mig_aggr:
        :return:
        """
        START_YEAR = 2018
        END_YEAR = 2038
        x = np.arange(START_YEAR,END_YEAR,1)
        x0 = x.copy()-0.1
        x2 = x.copy()+0.1
        texFigure(6,4,1,12,100)
        plt.step(x0,mig_cons, color='xkcd:purple',label = 'Conservative')
        plt.step(x,[val+1 for val in mig_likely], color='xkcd:orange',label = 'Likely')
        plt.step(x2,[val+2 for val in mig_aggr], color='xkcd:dark teal',label = 'Aggressive')
        if index==0:
            title = '100 Mbps provided by FTTC/FTTB/FTTH\nMigrations to 100 Mbps not forced'
        elif index == 1:
            title = '100 Mbps provided by FTTH\nMigrations to 100 Mbps not forced'
        elif index == 2:
            title= '100 Mbps provided by FTTC/FTTB/FTTH\nMigrations to 100 Mbps forced at 2025'
        else:
            title = '100 Mbps provided by FTTH\nMigrations to 100 Mbps forced at 2025'

        plt.suptitle(title)
        plt.xticks(np.arange(2018,2038,step=2))
        plt.yticks([0,20,50,100,120])
        plt.ylabel('Average Datarate in Mbps')
        plt.grid(True,which='major',axis='x',color='blue',linestyle='--')
        plt.legend()
        texSaveFig("mig_step"+str(index)+".pdf")

    def make_fig_steps_comp_cost(self,index,mig_cons,mig_likely,mig_aggr):
        """

        :param mig_cons:
        :param mig_likely:
        :param mig_aggr:
        :return:
        """
        START_YEAR = 2018
        END_YEAR = 2038
        x = np.arange(START_YEAR,END_YEAR,1)
        x0 = x.copy()-0.1
        x2 = x.copy()+0.1
        texFigure(6,4,1,12,100)
        plt.step(x0,mig_cons, color='xkcd:purple',label = 'Conservative')
        plt.step(x,[val+1 for val in mig_likely], color='xkcd:orange',label = 'Likely')
        plt.step(x2,[val+2 for val in mig_aggr], color='xkcd:dark teal',label = 'Aggressive')
        if index==0:
            title = 'Migration Steps for OASE Base Model'
        elif index == 1:
            title = 'Migration Steps for OASE new OPEX'
        elif index == 2:
            title= 'Migration Steps for Rokkas'
        else:
            title = 'Migration Steps for BSG'

        plt.suptitle(title)
        plt.xticks(np.arange(2018,2038,step=2))
        plt.yticks([0,20,50,100,120])
        plt.ylabel('Average Datarate in Mbps')
        plt.grid(True,which='major',axis='x',color='blue',linestyle='--')
        plt.legend()
        texSaveFig("mig_step_new_opex"+str(index)+".pdf")

    def create_migration_steps(self, scenario=0):
        """
        Datarate vs year of migration for all 12 different cases
        :param scenario: 0:residential, 1:business, 2:ITS
        :return:
        """

        data_rate = {u'ADSL': 20, u'FTTC_GPON_25': 30, u'FTTB_XGPON_50': 50, u'FTTB_UDWDM_50': 50,
                     u'FTTH_UDWDM_100': 100, u'FTTH_XGPON_100': 100, u'FTTC_GPON_100': 100, u'FTTB_XGPON_100': 100,
                     u'FTTB_UDWDM_100': 100, u'FTTC_Hybridpon_25': 30, u'FTTB_Hybridpon_50': 50,
                     u'FTTH_Hybridpon_100': 100, u'FTTC_Hybridpon_100': 100, u'FTTB_Hybridpon_100': 100}
        if scenario == 0:

            results_json_file = os.path.join(self.json_dir,self.residential_json_file)
            scenario_name = 'residential'
        elif scenario == 1:
            results_json_file = os.path.join(self.json_dir,self.business_json_file)
            scenario_name = 'business+residential'
        else:
            results_json_file = os.path.join(self.json_dir,self.its_json_file)
            scenario_name = 'ITS+business+residential'
        with open(results_json_file) as jsonfile:
            migration_data = json.load(jsonfile)

        index = 0
        x_col = 0
        y_col = 0
        mig_years = {}
        START_YEAR = 2018
        END_YEAR = 2038
        x = np.arange(START_YEAR,END_YEAR,1)

        # f, axarr = plt.subplots(2, 2)
        # plt.suptitle('Average datarates to customers during 15 year migration window: Scenario {0}'.format(scenario_name))
        mig_tree_cons = []
        mig_tree_likely = []
        mig_tree_aggr = []
        for ftth_flag in ['false','true']:

            for forced_depth in ['25','7']:

                for pen_curve in ['Cons PV', 'Likely PV', 'Aggr PV']:
                    mig_tree = migration_data[index]['migration_info'][pen_curve]['mig_path']
                    if pen_curve == 'Cons PV':
                        for tech in mig_tree:
                            mig_tree_cons.append(data_rate[tech])
                        mig_years['Conservative'] = json.dumps(migration_data[index]['migration_info'][pen_curve]['mig_years'],sort_keys=True)
                    elif pen_curve == 'Likely PV':
                        for tech in mig_tree:
                            mig_tree_likely.append(data_rate[tech])
                        mig_years['Likely'] = json.dumps(migration_data[index]['migration_info'][pen_curve]['mig_years'], sort_keys=True)
                    else:
                        for tech in mig_tree:
                            mig_tree_aggr.append(data_rate[tech])
                        mig_years['Aggressive'] = json.dumps(migration_data[index]['migration_info'][pen_curve]['mig_years'],sort_keys=True)
                # all three filled

                mig_tree_cons = self.len_check(mig_tree_cons,START_YEAR,END_YEAR)
                mig_tree_likely = self.len_check(mig_tree_likely,START_YEAR,END_YEAR)
                mig_tree_aggr = self.len_check(mig_tree_aggr,START_YEAR,END_YEAR)
                self.make_fig_steps(index,mig_tree_cons,mig_tree_likely,mig_tree_aggr)
                mig_tree_cons = []
                mig_tree_likely = []
                mig_tree_aggr = []
                index += 1

    def mig_steps_comp_cost(self):
        data_rate = {u'ADSL': 20, u'FTTC_GPON_25': 30, u'FTTB_XGPON_50': 50, u'FTTB_UDWDM_50': 50,
                     u'FTTH_UDWDM_100': 100, u'FTTH_XGPON_100': 100, u'FTTC_GPON_100': 100, u'FTTB_XGPON_100': 100,
                     u'FTTB_UDWDM_100': 100, u'FTTC_Hybridpon_25': 30, u'FTTB_Hybridpon_50': 50,
                     u'FTTH_Hybridpon_100': 100, u'FTTC_Hybridpon_100': 100, u'FTTB_Hybridpon_100': 100}
        with open(os.path.join(self.json_dir,r"results_comp_cost.json")) as jsonfile:
            migration_data = json.load(jsonfile)
        index = 0
        mig_years = {}
        START_YEAR = 2018
        END_YEAR = 2038
        x = np.arange(START_YEAR,END_YEAR,1)
        mig_tree_cons = []
        mig_tree_likely = []
        mig_tree_aggr = []
        for name in ['OASE','Phillipson','Rokkas','BSG']:# ['OASE Base Model','OASE new OPEX']:# ['OASE','Phillipson','Rokkas','BSG']:
                for pen_curve in ['Cons PV', 'Likely PV', 'Aggr PV']:
                    mig_tree = migration_data[index]['migration_info'][pen_curve]['mig_path']
                    if pen_curve == 'Cons PV':
                        for tech in mig_tree:
                            mig_tree_cons.append(data_rate[tech])
                        mig_years['Conservative'] = json.dumps(migration_data[index]['migration_info'][pen_curve]['mig_years'],sort_keys=True)
                    elif pen_curve == 'Likely PV':
                        for tech in mig_tree:
                            mig_tree_likely.append(data_rate[tech])
                        mig_years['Likely'] = json.dumps(migration_data[index]['migration_info'][pen_curve]['mig_years'], sort_keys=True)
                    else:
                        for tech in mig_tree:
                            mig_tree_aggr.append(data_rate[tech])
                        mig_years['Aggressive'] = json.dumps(migration_data[index]['migration_info'][pen_curve]['mig_years'],sort_keys=True)
                # all three filled

                mig_tree_cons = self.len_check(mig_tree_cons,START_YEAR,END_YEAR)
                mig_tree_likely = self.len_check(mig_tree_likely,START_YEAR,END_YEAR)
                mig_tree_aggr = self.len_check(mig_tree_aggr,START_YEAR,END_YEAR)
                self.make_fig_steps_comp_cost(index,mig_tree_cons,mig_tree_likely,mig_tree_aggr)
                mig_tree_cons = []
                mig_tree_likely = []
                mig_tree_aggr = []
                index += 1


if __name__ == "__main__":

    grapher = OutputGraphs(os.path.join(os.getcwd(),'..','..'))
    scenario = sys.argv[1]
    if scenario == 'residential':
        scen_int = 0
    elif scenario == 'business':
        scen_int = 1
    else:
        scen_int = 2
    # grapher.create_npv_graph(scen_int)
    # grapher.create_migration_steps(scen_int)
    # grapher.churn_npv()
    grapher.comp_cost_npv()
   #  grapher.mig_steps_comp_cost()
