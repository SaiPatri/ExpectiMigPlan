"""
Creates the following graphs:
1. Net Present Values in residential scenario for all cases
2. Net Present Values in business scenario for all cases
"""
import json
import os
import numpy as np
import matplotlib.pyplot as plt
import sys
from collections import OrderedDict

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
        elif scenario == 1:
            results_json_file = os.path.join(self.json_dir,self.business_json_file)
        else:
            results_json_file = os.path.join(self.json_dir,self.its_json_file)
        with open(results_json_file) as jsonfile:
            migration_data = json.load(jsonfile)
        expected_npv_cons = []
        expected_npv_likely = []
        expected_npv_aggr = []
        # Set up the graph
        # no. of scenarios is 4, each scenario has 3 bars
        index_bar = np.arange(4)
        width = 0.25
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

        rects_cons = ax.bar(index_bar,expected_npv_cons,width,color='r')
        rects_likely = ax.bar(index_bar+width,expected_npv_likely,width,color='b')
        rects_aggr = ax.bar(index_bar+2*width,expected_npv_aggr,width,color='g')

        ax.set_ylabel('Net Present Value in Cost Units')
        ax.set_title('Expected NPV in residential scenario for different penetration curves')
        ax.set_xticks(index_bar + width/3)
        ax.set_yticks(np.arange(np.floor(min(expected_npv_cons)/1000.0)*1000.0-100000.0,np.ceil(max(expected_npv_aggr)/1000.0)*1000.0+200000.0,100000.0))
        ax.set_xticklabels(('Unforced to 100 Mbps\nFTTC/FTTB/FTTH', 'Unforced to 100 Mbps\nOnly FTTH', 'Forced to 100 Mbps in 2025\nFTTC/FTTB/FTTH','Forced to 100 Mbps in 2025\nOnly FTTH'))
        ax.legend((rects_cons[0], rects_likely[0], rects_aggr[0]), ('Conservative Penetration', 'Likely Penetration','Aggressive Penetration'))

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
        plt.show(block=False)

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

    def create_migration_steps(self,scenario=0):
        """
        Datarate vs year of migration for all 12 different cases
        :param scenario: 0:residential, 1:business, 2:ITS
        :return:
        """

        data_rate = {u'ADSL': 20, u'FTTC_GPON_25': 25, u'FTTB_XGPON_50': 50, u'FTTB_UDWDM_50': 50,
                     u'FTTH_UDWDM_100': 100, u'FTTH_XGPON_100': 100, u'FTTC_GPON_100': 100, u'FTTB_XGPON_100': 100,
                     u'FTTB_UDWDM_100': 100, u'FTTC_Hybridpon_25': 25, u'FTTB_Hybridpon_50': 50,
                     u'FTTH_Hybridpon_100': 100, u'FTTC_Hybridpon_100': 100, u'FTTB_Hybridpon_100': 100}
        if scenario == 0:

            results_json_file = os.path.join(self.json_dir,self.residential_json_file)
        elif scenario == 1:
            results_json_file = os.path.join(self.json_dir,self.business_json_file)
        else:
            results_json_file = os.path.join(self.json_dir,self.its_json_file)
        with open(results_json_file) as jsonfile:
            migration_data = json.load(jsonfile)

        index = 0
        x_col = 0
        y_col = 0
        mig_years = {}
        START_YEAR = 2018
        END_YEAR = 2030
        x = np.arange(START_YEAR,END_YEAR,1)
        x0 = x.copy()-0.2
        x2 = x.copy()+0.2
        f, axarr = plt.subplots(2, 2)
        plt.suptitle('Average datarates to customers during 15 year migration window')
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

                """
                while True:
                    if (len(mig_tree_cons) == 15) and (len(mig_tree_likely) == 15) and (len(mig_tree_aggr) == 15):
                        break
                    elif len(mig_tree_cons) > 15:
                        mig_tree_cons.pop(-1)
                    elif len(mig_tree_likely) > 15:
                        mig_tree_likely.pop(-1)
                    elif len(mig_tree_aggr) > 15:
                        mig_tree_aggr.pop(-1)
                """
                # mig_tree_data_rate = [val for val in data_rate[mig_tree.pop(0)]]
                mig_tree_cons = self.len_check(mig_tree_cons,START_YEAR,END_YEAR)
                mig_tree_likely = self.len_check(mig_tree_likely,START_YEAR,END_YEAR)
                mig_tree_aggr = self.len_check(mig_tree_aggr,START_YEAR,END_YEAR)

                axarr[x_col,y_col].step(x0,mig_tree_cons, color='red',label = 'Conservative Penetration')
                axarr[x_col,y_col].step(x,[val+2 for val in mig_tree_likely], color='blue',label = 'Likely Penetration')
                axarr[x_col,y_col].step(x2,[val+4 for val in mig_tree_aggr], color='green',label = 'Aggressive Penetration')
                if index==0:
                    title = '100 Mbps provided by FTTC/FTTB/FTTH\nMigrations to 100 Mbps are not forced'
                elif index == 1:
                    title = '100 Mbps provided by only FTTH\nMigrations to 100 Mbps are not forced'
                elif index == 2:
                    title= '100 Mbps provided by FTTC/FTTB/FTTH\nMigrations to 100 Mbps are forced at year 2025'
                else:
                    title = '100 Mbps provided by only FTTH\nMigrations to 100 Mbps are forced at year 2025'

                axarr[x_col, y_col].set_title(title)
                axarr[x_col,y_col].set_xlim(2017,2033,1)
                axarr[x_col,y_col].set_ylim(0,120)
                axarr[x_col,y_col].set_ylabel('Average Datarate in Mbps')
                axarr[x_col,y_col].grid(True,which='major',axis='x',color='blue',linestyle='--')
                text_to_add = ''
                sorted_mig_dict = OrderedDict(sorted(mig_years.items()))
                for key,value in sorted_mig_dict.items():
                    text_to_add += key+':  '+mig_years[key]+'\n'
                axarr[x_col,y_col].text(0.5,0.04,text_to_add,va='bottom', ha='center', fontsize=9,weight='semibold',transform=axarr[x_col,y_col].transAxes)
                axarr[x_col,y_col].legend(loc='center right')
                index += 1
                y_col += 1
                if y_col ==2:
                    y_col = 0
                mig_tree_cons = []
                mig_tree_likely = []
                mig_tree_aggr = []
            x_col += 1
            if x_col == 2:
                x_col = 0


        plt.show()


if __name__ == "__main__":

    grapher = OutputGraphs(os.path.join(os.getcwd(),'..\\..'))
    scenario = sys.argv[1]
    if scenario == 'residential':
        scen_int = 0
    elif scenario == 'business':
        scen_int = 1
    else:
        scen_int = 2
    grapher.create_npv_graph(scen_int)
    grapher.create_migration_steps(scen_int)
