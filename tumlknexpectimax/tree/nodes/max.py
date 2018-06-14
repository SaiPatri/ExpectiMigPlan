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
        self.cust_dict = {
            'Cons PV': [96, 128, 172, 233, 318, 435, 594, 813, 1109, 1509, 2044, 2751, 3672, 4849, 6311, 8068, 10087,
                        12287, 14535, 16674, 18559],
            'Likely PV': [96, 132, 183, 257, 363, 514, 727, 1027, 1446, 2028, 2822, 3887, 5281, 7042, 9166, 11580,
                          14126, 16582, 18730, 20431, 21658],
            'Aggr PV': [96, 179, 342, 661, 1284, 2473, 4660, 8373, 13760, 19517, 22973, 23713, 23747, 23753, 23756,
                        23758, 23759, 23759, 23760, 23760, 23760]
        }
        self.next_terminal = None
        self.next_chancer = None

        pass

    def maximizer(self, type, node_technology,depth,children,churn_rate,prob_churn):
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
            if depth < 10:
                capex_rev_terminal = -(self.capex_values_dict['Electronic Cost'][self.techindex[node_technology]])
            return [sum([self.next_terminal.terminal_node(node_technology,dep,churn_rate) for dep in range(depth, 2038-self.START_YEAR)])+capex_rev_terminal, depth, node_technology,'NONE', []]    # Returns the value of the PV cashflow along with a list of the [depth, technology_of_terminal, child_of_terminal, previous_list]
        elif node_technology in [4, 5, 6, 7, 8, 11, 12, 13]:
            # TODO: Need to check here if we can try to find the sum value of the remainder years and whether it affects our decision
            self.next_terminal = TerminalNode(self.pen_curve,self.START_YEAR,self.cust_dict[self.pen_curve],self.pv)
            if depth < 10:
                capex_rev_terminal = -(self.capex_values_dict['Electronic Cost'][self.techindex[node_technology]])
            return [sum([self.next_terminal.terminal_node(node_technology,dep,churn_rate) for dep in range(depth, 2038-self.START_YEAR)])+capex_rev_terminal, depth, node_technology,'NONE', []]
        else:
            self.next_chancer = ChanceNode(self.node_mig_dict_forced, self.node_mig_dict_unforced,
                                           self.capex_values_dict, self.techindex, self.mig_matrix, self.pen_curve,
                                           self.path_list, self.force_depth,self.START_YEAR, self.MAX_YEAR,self.pv)
            max_derived_cf = -1000000000
            temp_dict = {}
            max_child_tech = node_technology
            max_child_list = []
            if depth >= self.force_depth-1:
                current_child_list = self.node_mig_dict_forced[node_technology]
            else:
                current_child_list = self.node_mig_dict_unforced[node_technology]
            for child_technology in current_child_list:

                if child_technology is node_technology:

                    if depth == 10: # child_technology is node_technology
                        capex_rev = -(self.capex_values_dict['Electronic Cost'][self.techindex[node_technology]])
                    else:
                        capex_rev = 0
                else:
                    if depth == 10:

                        capex_rev = -self.capex_values_dict['Electronic Cost'][self.techindex[node_technology]] -self.mig_matrix[self.techindex[child_technology]][self.techindex[node_technology]]
                    else:
                        capex_rev = -self.mig_matrix[self.techindex[child_technology]][self.techindex[node_technology]]

                if type is 'MAXNOCHURN':
                    child_details = self.next_chancer.chancer(child_technology, depth+1, current_child_list, prob_churn)
                else:
                    child_details = self.next_chancer.chancer(child_technology, depth+1, current_child_list, prob_churn)

                future_cf = child_details[0]
                if isinstance(child_details[1:][0],list):

                    child_list_maxnodes = child_details[1:][0]
                else:
                    child_list_maxnodes = child_details[1:]
                if churn_rate == 0:
                    # curr_cf = self.pv_dict[node_technology][self.pen_curve][current_year]
                    curr_cf = self.pv.PV_no_churn(self.START_YEAR, depth, self.cust_dict[self.pen_curve][depth], node_technology)
                else:
                    # curr_cf = self.pv_dict[node_technology][self.pen_curve+'_churn'][current_year]
                    curr_cf = self.pv.PV_churn(self.START_YEAR,depth,churn_rate, self.cust_dict[self.pen_curve][depth],node_technology)

                derived_cf = capex_rev+curr_cf+future_cf
                temp_dict[child_technology] = child_list_maxnodes
                if derived_cf > max_derived_cf:
                    max_derived_cf = derived_cf
                    max_child_tech = child_technology
                    max_child_list = temp_dict[max_child_tech]
            self.path_list.append(max_child_list)

            return [max_derived_cf, depth, node_technology, max_child_tech, max_child_list]
