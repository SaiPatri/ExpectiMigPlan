
import math
from collections import OrderedDict
class GeneratePresentValue:

    def __init__(self,type,pen_curve,irr,capex,opex):
        """
        Generate present value with and without churn
        :param type:
        :param tech_index:
        :param pen_curve:
        :param year:
        :param opex:
        :param irr:
        """
        self.type = type
        self.rev_dict_residential = {0:3.6,1:7.2,2:9.6,3:9.6,4:12,5:12,6:12,7:12,8:12,9:7.2,10:9.6,11:12,12:12,13:12}
        self.rev_dict_business = {0:3.6,1:12,2:24,3:24,4:36,5:36,6:36,7:36,8:36,9:12,10:24,11:36,12:36,13:36}
        self.its_onetime = 800*12/50.0
        self.its_yearly = 150*12/50.0
        self.pen_curve = pen_curve
        self.irr = irr
        self.capex = capex
        self.opex = opex
        self.no_its_demands = 8
        self.techindex_dict = {0: u'ADSL', 1: u'FTTC_GPON_25', 2: u'FTTB_XGPON_50', 3: u'FTTB_UDWDM_50',
                          4: u'FTTH_UDWDM_100', 5: u'FTTH_XGPON_100', 6: u'FTTC_GPON_100',
                          7: u'FTTB_XGPON_100', 8: u'FTTB_UDWDM_100', 9: u'FTTC_Hybridpon_25',
                          10: u'FTTB_Hybridpon_50', 11: u'FTTH_Hybridpon_100', 12: u'FTTC_Hybridpon_100',
                          13: u'FTTB_Hybridpon_100'}

    def PV_churn(self,startyear,index,churn_rate,no_customers,tech_index):
        """

        :param churn_probability:
        :param no_customers:
        :param tech_index:
        :return:
        """

        rate = 1/math.pow(1+self.irr,index)
        current_opex = self.opex[self.techindex_dict[tech_index]]

        if self.type == 'residential':
            post_churn_customers = int(no_customers - churn_rate * no_customers)
            yearly_rev = post_churn_customers*self.rev_dict_residential[tech_index]

            current_cashflow = yearly_rev-current_opex

        elif self.type == 'business':
            # Since 7% of customers are business
            business_customers = math.floor(0.07*no_customers)
            residential_customers = math.ceil(no_customers-business_customers)
            post_churn_business_cust = int(business_customers-churn_rate*business_customers)
            post_churn_residential_cust = int(residential_customers-churn_rate*residential_customers)
            yearly_rev = post_churn_residential_cust*self.rev_dict_residential[tech_index]+\
                         post_churn_business_cust*self.rev_dict_business[tech_index]
            current_cashflow = yearly_rev-current_opex
        else:
            business_customers = math.floor(0.07 * no_customers)
            residential_customers = math.ceil(no_customers - business_customers)
            post_churn_business_cust = int(business_customers - churn_rate * business_customers)
            post_churn_residential_cust = int(residential_customers - churn_rate * residential_customers)
            if index < 7:
                yearly_rev = post_churn_residential_cust * self.rev_dict_residential[tech_index] \
                             + post_churn_business_cust * self.rev_dict_business[tech_index]

            elif index == 7:

                yearly_rev = post_churn_residential_cust * self.rev_dict_residential[tech_index] + \
                             post_churn_business_cust * self.rev_dict_business[tech_index]+ \
                             self.no_its_demands*(self.its_onetime+self.its_yearly)

            else:
                yearly_rev = post_churn_residential_cust * self.rev_dict_residential[tech_index] + \
                             post_churn_business_cust * self.rev_dict_business[tech_index] + \
                             self.no_its_demands*self.its_yearly

            current_cashflow = yearly_rev - current_opex

        pv_churn = current_cashflow*rate

        return pv_churn

    def PV_no_churn(self, startyear, index, no_customers, tech_index):

        rate = 1 / math.pow(1 + self.irr, index)
        current_opex = self.opex[self.techindex_dict[tech_index]]

        if self.type == 'residential':
            no_customers = int(no_customers)
            yearly_rev = no_customers * self.rev_dict_residential[tech_index]

            current_cashflow = yearly_rev - current_opex

        elif self.type == 'business':
            # Since 7% of customers are business
            business_customers = math.floor(0.07 * no_customers)
            residential_customers = math.ceil(no_customers - business_customers)
            business_cust = int(business_customers)
            residential_cust = int(residential_customers)
            yearly_rev = residential_cust * self.rev_dict_residential[tech_index] + \
                         business_cust * self.rev_dict_business[tech_index]
            current_cashflow = yearly_rev - current_opex
        else:
            business_customers = math.floor(0.07 * no_customers)
            residential_customers = math.ceil(no_customers - business_customers)
            business_cust = int(business_customers)
            residential_cust = int(residential_customers)
            if index < 7:

                yearly_rev = residential_cust * self.rev_dict_residential[
                    tech_index] + business_cust * self.rev_dict_business[tech_index]

            elif index == 7:

                yearly_rev = residential_cust * self.rev_dict_residential[
                    tech_index] + business_cust * self.rev_dict_business[
                                 tech_index] + self.no_its_demands * (self.its_onetime + self.its_yearly)

            else:
                yearly_rev = residential_cust * self.rev_dict_residential[
                    tech_index] + business_cust * self.rev_dict_business[
                                 tech_index] + self.no_its_demands * self.its_yearly

            current_cashflow = yearly_rev - current_opex

        pv_no_churn = current_cashflow * rate

        return pv_no_churn

    def rank_child_nodes(self,current_node,complete_child_list):
        """
        Sends the best 4 nodes
        :param type:
        :param current_node:
        :param complete_child_list:
        :return:
        """
        scaling_factor = 0.01
        if self.type == 'residential':
            no_hh = 29262
            revenue = self.rev_dict_residential
        elif self.type == 'business':
            no_hh = math.ceil(0.93*4877*6)+math.ceil(0.07*4877*6)
            revenue = self.rev_dict_business
        else:
            no_hh = math.ceil(0.93*(1.1*4877)*6)+math.ceil(0.07*4877*6)
            revenue = self.rev_dict_business

        current_capex = self.capex['Total Cost'][self.techindex_dict[current_node]]
        current_cost_hh = current_capex/float(no_hh)
        child_dict = {} # Child node and rank
        for child in complete_child_list:
            child_dict[child] = 1e10
        child_dict_ordered = OrderedDict(child_dict.items())
        for child in complete_child_list:
            child_cost_hh = self.capex['Total Cost'][self.techindex_dict[child]]/float(no_hh)
            if child_cost_hh-current_cost_hh > 100:
                continue
            else:
                penalty = scaling_factor*math.pow(child_cost_hh-current_cost_hh,2)  # square for severe penalty
                child_dict_ordered[child] = (child_cost_hh/float(revenue[child]))+penalty
        # find smallest 4 child tech

        # first find the smallest technology
        best_children = []
        while True:
            if len(best_children) == 4:
                break
            elif not child_dict_ordered:
                break
            else:
                #get minimum key value
                best_children.append(min(child_dict_ordered, key=child_dict_ordered.get))
                #delete minimum value from dict
                child_dict_ordered.pop(min(child_dict_ordered, key=child_dict_ordered.get))

        return best_children









