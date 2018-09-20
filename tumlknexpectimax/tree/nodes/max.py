

from tumlknexpectimax.tree.nodes.chance import ChanceNode
from tumlknexpectimax.tree.nodes.terminal import TerminalNode


class MaxNode:

    def __init__(self, node_mig_dict_forced, node_mig_dict_unforced,capex_values,tech_index, mig_matrix,
                 pen_curve, path_list, forcing_depth, start_year, max_year, pv):
        """

        """
        self.START_YEAR = start_year
        self.MAX_YEAR = max_year
        self.node_mig_dict_forced = node_mig_dict_forced
        self.node_mig_dict_unforced = node_mig_dict_unforced
        self.capex_values_dict = capex_values
        self.techindex = tech_index
        self.mig_matrix = mig_matrix
        self.pen_curve = pen_curve
        self.path_list = path_list
        self.force_depth = int(forcing_depth)
        self.pv = pv
        # MUNICH

        self.cust_dict = {
            'Cons PV': [96, 128, 172, 233, 318, 435, 594, 813, 1109, 1509, 2044, 2751, 3672, 4849, 6311, 8068, 10087,
                        12287, 14535, 16674, 18559],
            'Likely PV': [96, 132, 183, 257, 363, 514, 727, 1027, 1446, 2028, 2822, 3887, 5281, 7042, 9166, 11580,
                          14126, 16582, 18730, 20431, 21658],
            'Aggr PV': [96, 179, 342, 661, 1284, 2473, 4660, 8373, 13760, 19517, 22973, 23713, 23747, 23753, 23756,
                        23758, 23759, 23759, 23760, 23760, 23760]
        }
        """
        # NEWYORK
        
        self.cust_dict = {
            'Cons PV': [208, 276, 371, 504, 687, 938, 1284, 1755, 2394, 3257, 4412, 5938, 7927, 10467, 13623, 17414, 21773,
                        26521, 31374, 35990, 40058],
            'Likely PV': [208, 285, 396, 556, 784, 1109, 1569, 2217, 3123, 4377, 6091, 8391, 11399, 15200, 19785, 24996,
                          30490, 35792, 40429, 44099, 46749],
            'Aggr PV': [208, 387, 739, 1428, 2771, 5338, 10058, 18073, 29701, 42126, 49586, 51184, 51258, 51269, 51276,
                        51280, 51282, 51283,51284, 51285, 51285]
        }
        
        # OTTOBRUNN
        self.cust_dict = {
            'Cons PV': [29, 38, 51, 70, 95, 131, 179, 244, 334, 454, 615, 828, 1106, 1460, 1900, 2429, 3038, 3700, 4377, 5021, 5589],
            'Likely PV': [29, 39, 55, 77, 109, 154, 219, 309, 435, 610, 850, 1170, 1590, 2120, 2760, 3487, 4254, 4994, 5641, 6153, 6523],
            'Aggr PV': [29, 54, 103, 199, 386, 744, 1403, 2521, 4144, 5878, 6919, 7142, 7152, 7153, 7154, 7155, 7155, 7155, 7155, 7156, 7156]
        }
        """
        self.next_terminal = None
        self.next_chancer = None
        self.child_details = None
        self.curr_cf = None
        self.mig_adj_matrix = {'civil_elec': [(0,1), (0,2), (0,3), (0,4), (0,5), (0,6), (0,7), (0,8), (0,9), (0,10),
                                              (0,11),(0,12), (0,13), (1,2), (1,5), (1,7), (2,5), (3,4), (6,5), (6,7),
                                              (9,10), (9,11), (9,13), (10,11)],
                               'civil': [(7,5), (8,4), (12,11), (12,13)],
                               'elec': [(1,6), (2,7), (3,8),(9,12), (10,13), (13,11)]
                               }



    def find_best_children(self,current_node,complete_child_list):
        """

        :param current_node:
        :param complete_child_list:
        :return:
        """
        best_children = self.pv.rank_child_nodes(current_node,complete_child_list)
        return best_children

    def mig_cost(self, node_tech,child_tech):
        """
        Uses various component costs of two technologies to generate an accurate migration cost
        :param node_tech:
        :param child_tech:
        :return: migration_cost
        """
        if node_tech == child_tech:
            return 0

        elif node_tech == 0:
            return self.capex_values_dict['Total Cost'][self.techindex[child_tech]]
        else:

            mig_tuple = (node_tech,child_tech)
            mig_config = 'not_found'

            for key,val in self.mig_adj_matrix.items():
                if mig_tuple in val:
                    mig_config = key

            if mig_config == 'civil_elec': # for eg FTTC_GPON_25 to FTTB_XGPON_50

                mig_cost = self.capex_values_dict['Total Cost'][self.techindex[child_tech]] - \
                           self.capex_values_dict['Total Cost'][self.techindex[node_tech]]
                # First check the difference in capex
                if mig_cost < 0:
                    mig_cost = self.capex_values_dict['Duct Cost'][self.techindex[child_tech]] + \
                               self.capex_values_dict['Fiber Cost'][self.techindex[child_tech]] - \
                               self.capex_values_dict['Duct Cost'][self.techindex[node_tech]] - \
                               self.capex_values_dict['Fiber Cost'][self.techindex[node_tech]] + \
                               self.capex_values_dict['Electronic Cost'][self.techindex[child_tech]]
                    # if difference in capex goes negative, just find difference in civil works and add
                    # total electronic cost to it

            elif mig_config == 'civil':
                # For eg FTTB_UDWDM_50 to FTTH_UDWDM_100
                mig_cost = self.capex_values_dict['Duct Cost'][self.techindex[child_tech]] + \
                           self.capex_values_dict['Fiber Cost'][self.techindex[child_tech]] - \
                           self.capex_values_dict['Duct Cost'][self.techindex[node_tech]] - \
                           self.capex_values_dict['Fiber Cost'][self.techindex[node_tech]]

            elif mig_config == 'elec':
                # For eg FTTC_GPON_25 to FTTC_GPON_100

                mig_cost = self.capex_values_dict['Electronic Cost'][self.techindex[child_tech]] - \
                           self.capex_values_dict['Electronic Cost'][self.techindex[node_tech]]
                if mig_cost < 0:
                    mig_cost = self.capex_values_dict['Electronic Cost'][self.techindex[child_tech]]
            else:
                print('The migration from {0} to {1} is not allowed!!'.format(self.techindex[node_tech],
                                                                              self.techindex[child_tech]))
                mig_cost = 1e55

            return mig_cost

    def maximizer(self, type, node_technology,depth,children,churn_rate,mean_prob):
        """

        :param type:
        :param node_technology:
        :param depth:
        :param children:
        :param churn_rate:
        :param prob_churn:
        :return:
        """
        current_year = self.START_YEAR+depth
        capex_rev_terminal = 0

        if current_year == self.MAX_YEAR:   # If we have reached max year we should hit a terminal node

            self.next_terminal = TerminalNode(self.pen_curve,self.START_YEAR,self.cust_dict[self.pen_curve],self.pv)
            if depth >= 9:
                capex_rev_terminal = -(self.capex_values_dict['Electronic Cost'][self.techindex[node_technology]])
            total_rev = [sum([self.next_terminal.terminal_node(node_technology,dep,churn_rate) for dep in range(depth, 2038-self.START_YEAR)])+capex_rev_terminal, depth, node_technology,'NONE', []]    # Returns the value of the PV cashflow along with a list of the [depth, technology_of_terminal, child_of_terminal, previous_list]
            return total_rev

        elif node_technology in [4, 5, 6, 7, 8, 11, 12, 13]: # If we have reached final technology we should hit a terminal node

            self.next_terminal = TerminalNode(self.pen_curve,self.START_YEAR,self.cust_dict[self.pen_curve],self.pv)
            if depth >= 9:
                capex_rev_terminal = -(self.capex_values_dict['Electronic Cost'][self.techindex[node_technology]])
            total_rev = [sum([self.next_terminal.terminal_node(node_technology,dep,churn_rate) for dep in range(depth, 2038-self.START_YEAR)])+capex_rev_terminal, depth, node_technology,'NONE', []]
            return total_rev
        else:
            self.next_chancer = ChanceNode(self.node_mig_dict_forced, self.node_mig_dict_unforced,
                                           self.capex_values_dict, self.techindex, self.mig_matrix, self.pen_curve,
                                           self.path_list, self.force_depth,self.START_YEAR, self.MAX_YEAR,self.pv)
            max_derived_cf = -1000000000
            temp_dict = {}
            max_child_tech = node_technology
            max_child_list = []
            if depth > self.force_depth-1:
                current_child_list = self.node_mig_dict_forced[node_technology]
            else:
                current_child_list = self.node_mig_dict_unforced[node_technology]
            if depth > 10:
                current_child_list = self.find_best_children(node_technology,current_child_list)
            for child_technology in current_child_list:

                capex_rev = 0

                if child_technology == node_technology:

                    if depth == self.force_depth: # child_technology is node_technology
                        capex_rev = - self.capex_values_dict['Electronic Cost'][self.techindex[node_technology]]

                else:
                    if depth == self.force_depth:

                        capex_rev = - self.capex_values_dict['Electronic Cost'][self.techindex[node_technology]] - \
                                    self.mig_cost(node_technology,child_technology)
                    else:
                        capex_rev = -self.mig_cost(node_technology,child_technology)

                if type is 'MAXNOCHURN':
                    self.child_details = self.next_chancer.chancer(child_technology, depth+1, current_child_list, mean_prob)
                else:
                    self.child_details = self.next_chancer.chancer(child_technology, depth+1, current_child_list, mean_prob)

                future_cf = self.child_details[0]
                if isinstance(self.child_details[1:][0],list):

                    child_list_maxnodes = self.child_details[1:][0]
                else:
                    child_list_maxnodes = self.child_details[1:]
                if churn_rate == 0:
                    # curr_cf = self.pv_dict[node_technology][self.pen_curve][current_year]
                    self.curr_cf = self.pv.PV_no_churn(self.START_YEAR, depth, self.cust_dict[self.pen_curve][depth], node_technology)
                else:
                    # curr_cf = self.pv_dict[node_technology][self.pen_curve+'_churn'][current_year]
                    self.curr_cf = self.pv.PV_churn(self.START_YEAR,depth,churn_rate, self.cust_dict[self.pen_curve][depth],node_technology)

                derived_cf = capex_rev+self.curr_cf+future_cf
                temp_dict[child_technology] = child_list_maxnodes
                if derived_cf > max_derived_cf:
                    max_derived_cf = derived_cf
                    max_child_tech = child_technology
                    max_child_list = temp_dict[max_child_tech]
            self.path_list.append(max_child_list)

            return [max_derived_cf, depth, node_technology, max_child_tech, max_child_list]
