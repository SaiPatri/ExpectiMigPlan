import json
import os
import scipy as sp
import scipy.stats
import matplotlib.pyplot as plt
import numpy as np

class ConfidencePlots:
    """

    """
    def __init__(self,result_directory):
        self.json_npv = os.path.join(result_directory,'results_expectimax_its_npv_variation_100.json')

    def mean_confidence_interval(self,data, confidence=0.95):
        a = 1.0*np.array(data)
        n = len(a)
        m, se = np.mean(a), scipy.stats.sem(a)
        h = se * sp.stats.t.ppf((1+confidence)/2., n-1)
        return m, m-h, m+h

    def plot_box(self):
        npv_cons = []
        npv_likely = []
        npv_aggr = []
        iteration = []
        with open(self.json_npv) as jsonfile:
            confidence_npv = json.load(jsonfile)

        for iter in range(1,100):
            for item in confidence_npv:
                if item["is_ftth_and_force"] == iter:
                    npv_cons.append(item["migration_info"]["Cons PV"]["NPV_expected"])
                    npv_likely.append(item["migration_info"]["Likely PV"]["NPV_expected"])
                    npv_aggr.append(item["migration_info"]["Aggr PV"]["NPV_expected"])

        data_to_plot = [npv_aggr]
        figure1= plt.figure(1,figsize=(10,6))
        ax = figure1.add_subplot(111)
        npv_box = ax.boxplot(data_to_plot,patch_artist=True)
        plt.xticks([1], ['Aggressive'])
        plt.xlabel('Customer Penetration Type')
        plt.ylabel('Net Present Value in Cost Units')
        plt.suptitle('Expectimax Search Results for 500 runs of Aggressive customer penetration at tree depth 10 years')
        median = np.median(data_to_plot)
        stat_list=[item.get_ydata(0) for item in npv_box['whiskers']]
        low_whisker = stat_list[0][0]
        low_quartile = stat_list[0][1]
        high_quartile = stat_list[1][0]
        high_whisker = stat_list[1][1]
        plt.text(0.1,0.2,'Upper Quartile: {0}\nMedian:{1}\nLowerQuartile: {2}\n'.format(high_quartile,median,low_quartile))
        items = [item.get_ydata() for item in npv_box['whiskers']]
        print items
        plt.show()
        # figure1.savefig(os.path.join(os.getcwd(),'..','npv_confidence_plots_aggr.png'),bbox_inches='tight')



if __name__== "__main__":
    Confi_NPV = ConfidencePlots(r'C:\Users\ga47kiw\PycharmProjects\mt_branch_new_code\tumlknexpectimax')
    Confi_NPV.plot_box()

    # print(len(npv_cons),len(npv_likely),len(npv_aggr))



